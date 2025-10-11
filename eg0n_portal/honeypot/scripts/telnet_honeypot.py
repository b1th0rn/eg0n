import os, sys, socket, datetime, json, random, string, requests, time, select, multiprocessing

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eg0n_portal.settings")
import django
django.setup()

from http.server import BaseHTTPRequestHandler, HTTPServer
from honeypot.models import telnet_log
from django.utils import timezone

# import apiConfig model to get Gemini API key
from core.models import apiConfig

# server configuration
HOST = '0.0.0.0'
TELNET_PORT = 23
BANNER = "Ubuntu 20.04.3 TLS\r\n"

def add_log(req_ip, req_port, req_username, req_password, req_command):
    telnet_log.objects.create(
        req_ip=req_ip,
        req_port=req_port,
        req_username=req_username,
        req_password=req_password,
        req_command=req_command,
        log_date=timezone.now().date(),
        slug='telnet-honeypot-log',
        author='honeypot',
        lastchange_author='honeypot'
    )

def clean_input(s: str) -> str:
    # remove non-printable characters
    return ''.join(c for c in s if c in string.printable and c not in '\x01\x03')

# remove IAC sequences
def recv_input(client_socket: socket.socket, echo: bool = True, timeout: int = 10) -> str:
    data = bytearray()
    iac_mode = False
    start_session = time.time()

    try:
        while True:
            time_left = timeout - (time.time() - start_session)
            if time_left <= 0:
                raise socket.timeout()

            rlist, _, _ = select.select([client_socket], [], [], time_left)
            if not rlist:
                raise socket.timeout()
            
            chunk = client_socket.recv(1)
            if not chunk:
                # Socket close by client
                raise ConnectionResetError("Socket closed by client")

            # IAC handling
            if chunk == b'\xff':
                iac_mode = True
                continue
            if iac_mode:
                # skip the next byte after IAC
                iac_mode = False
                continue

            # enter key (CR or LF)
            if chunk in (b'\r', b'\n'):
                # non-blocking read to clear any extra chars (like LF after CR)
                client_socket.setblocking(False)
                try:
                    next_char = client_socket.recv(1)
                    if next_char != b'\n':
                        if next_char:
                            data.extend(next_char)
                except Exception:
                    pass
                finally:
                    client_socket.setblocking(True)
                break

            # backspace handling
            if chunk in (b'\x08', b'\x7f'):
                if len(data) > 0:               # if there's something to delete
                    data = data[:-1]            # delete last char
                    if echo:                    # if echo is enabled, handle backspace on client side
                        client_socket.send(b'\b \b')    # backspace, space, backspace to erase char
                continue

            # only accept printable characters
            if 32 <= ord(chunk) <= 126:
                data.extend(chunk)
                if echo:
                    client_socket.send(chunk)

    except socket.timeout:
        return ""  # Timeout: return empty string
    except (ConnectionResetError, OSError):
        # in case of connection reset by peer or other socket errors
        raise
    except Exception:
        return ""

    raw_input = data.decode('utf-8', errors='ignore').strip()
    return clean_input(raw_input)

def get_shell_response_from_gemini(command: str) -> str:
    """
    send command to Gemini and get the response
    """

    # check for ampty command, return prompt and avoid API call
    if not command.strip():
        return "$ "

    api_key = apiConfig.objects.filter(api_name='GEMINI_test').first().api_key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    prompt = f"Simulate a Linux shell. Respond only with the command output, no explanations. In case of document to read such as TXT, LOG, CONF, INI, JSON, XML, YAML, CSV, HTML, PHP, PYTHON, JAVASCRIPT, BASH, SHELL SCRIPT, DOCKERFILE, KUBERNETES, return only the content of the file with techical information. Do not include any additional text or formatting. Here is the command: {command}"
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        # gemini returns the response in result['candidates'][0]['content']['parts'][0]['text']
        output = (
            result.get('candidates', [{}])[0]
            .get('content', {})
            .get('parts', [{}])[0]
            .get('text', '')
        )
        return output.strip() + "\r\n$ "
    except Exception as e:
        return f"Errore nell'interrogazione a Gemini: {e}\r\n$ "

# telnet server
def telnet_server(last_activity):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, TELNET_PORT))
    server_socket.listen(5) # max 5 connections in queue
    print(f"[*] Telnet honeypot listening on {HOST}:{TELNET_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        # timestamp last activity
        last_activity.value = time.time()

        try:

            # send banner
            client_socket.send(BANNER.encode('utf-8'))

            # login prompt
            client_socket.send(b"login: ")
            req_username = recv_input(client_socket, echo=True)
            add_log(addr[0], addr[1], req_username, 'none', 'Login Attempt')

            # password prompt
            client_socket.send(b"Password: ")
            ### echo ON for password input
            client_socket.send(b'\xFF\xFB\x01')  # IAC WILL ECHO
            client_socket.send(b'\xFF\xFE\x03')  # IAC DONT ECHO
            req_password = recv_input(client_socket, echo=False)
            ### echo ON after password input
            client_socket.send(b'\xFF\xFC\x01')  # IAC WONT ECHO
            client_socket.send(b'\xFF\xFD\x03')  # IAC DO ECHO
            add_log(addr[0], addr[1], req_username, req_password, 'Password Attempt')
            client_socket.send(b"\r\nWelcome to Ubuntu!\r\n$ ")

            while True:
                req_commnand = recv_input(client_socket, echo=False)
                if req_commnand.lower() in ['exit', 'quit', 'logout']:
                    client_socket.send(b"Logout\r\n")
                    break
                if req_commnand:
                    # use Gemini to simulate shell response
                    response = get_shell_response_from_gemini(req_commnand)
                    client_socket.send(response.encode('utf-8'))
                    add_log(addr[0], addr[1], req_username, req_password, req_commnand)
        
        except Exception as e:
            print(f"[*] Exception: {e}")
        finally:
            client_socket.close()
            print(f"[*] Closed connection from {addr[0]}:{addr[1]}")

# watchdog to close server after inactivity
def inactivity_watchdog():
    last_activity = multiprocessing.Value('d', time.time())

    while True:
        proc = multiprocessing.Process(target=telnet_server, args=(last_activity,)) # pass the shared value to the server process
        proc.start() # start the server process
        print("[*] Watchdog started the telnet server process.")

        while proc.is_alive():
            time.sleep(10) # check every 10 seconds
            if time.time() - last_activity.value > 120: # seconds of inactivity
                print("[*] No activity detected for 5 minutes. Terminating the telnet server process.")
                proc.terminate() # terminate the server process
                proc.join() # wait for the process to finish
                break
        
        if not proc.is_alive():
            print("[*] Telnet server process has stopped. Restarting...")
            time.sleep(5) # wait before restarting

# main
if __name__ == "__main__":
    try:
        inactivity_watchdog()
    except KeyboardInterrupt:
        print("\n[*] Shutting down the server.")
        sys.exit(0)