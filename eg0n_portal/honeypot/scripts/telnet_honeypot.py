import os, sys, socket, datetime, json, random, string

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eg0n_portal.settings")
import django
django.setup()

from http.server import BaseHTTPRequestHandler, HTTPServer
from honeypot.models import telnet_log
from django.utils import timezone

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
    # Rimuove caratteri non stampabili
    return ''.join(c for c in s if c in string.printable and c not in '\x01\x03')

# remove IAC sequences
def recv_input(client_socket: socket.socket, echo: bool = True) -> str:
    data = bytearray()
    iac_mode = False  # Modalità interpretazione comandi Telnet

    try:
        while True:
            chunk = client_socket.recv(1)
            if not chunk:
                break

            # Gestione sequenze IAC (Interpret As Command)
            if chunk == b'\xff':
                iac_mode = True
                continue
            if iac_mode:
                # Salta i byte di comando Telnet
                iac_mode = False
                continue

            # Gestione invio (Enter)
            if chunk in (b'\r', b'\n'):
                # Consuma eventuale LF dopo CR
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

            # Gestione backspace e delete
            if chunk in (b'\x08', b'\x7f'):
                if len(data) > 0:               # se c'è qualcosa da cancellare
                    data = data[:-1]            # rimuovi l'ultimo carattere  
                    if echo:                    # echo del backspace
                        client_socket.send(b'\b \b')    # sposta indietro, spazio, sposta indietro
                continue

            # Solo caratteri stampabili e backspace "32 <= chunk[0] <= 126:"
            if 32 <= ord(chunk) <= 126:
                data.extend(chunk)
                if echo:
                    client_socket.send(chunk)

    except Exception:
        pass

    raw_input = data.decode('utf-8', errors='ignore').strip()
    return clean_input(raw_input)

# telnet server
def telnet_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, TELNET_PORT))
    server_socket.listen(5)
    print(f"[*] Telnet honeypot listening on {HOST}:{TELNET_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        try:

            # send banner
            client_socket.send(BANNER.encode('utf-8'))

            # login prompt
            client_socket.send(b"login: ")
            req_username = recv_input(client_socket, echo=False)
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
                req_commnand = recv_input(client_socket, echo=False) # echo ON for command input
                if req_commnand.lower() in ['exit', 'quit', 'logout']:
                    client_socket.send(b"Logout\r\n")
                    break
                if req_commnand:
                    response = f"bash: {req_commnand}: command not found\r\n$ "
                    client_socket.send(response.encode('utf-8'))
                    add_log(addr[0], addr[1], req_username, req_password, req_commnand)
        
        except Exception as e:
            print(f"[*] Exception: {e}")
        finally:
            client_socket.close()
            print(f"[*] Closed connection from {addr[0]}:{addr[1]}")

# funziona mail
if __name__ == "__main__":
    try:
        telnet_server()
    except KeyboardInterrupt:
        print("\n[*] Shutting down the server.")
        sys.exit(0)