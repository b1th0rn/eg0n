import os, sys, socket, datetime, time, threading

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

# receive command from client
def process_command(command):

    # exit command -- close connection
    if command.strip() in ['exit', 'logout', 'quit']:
        return 'exit'
    
    #
    # LLM integration...
    # 

    # temporary response
    output = f"bash: {command}: command not found\r\n"
    return output

def handle_client(client_socket, client_address, timeout=10):
    
    # new connection
    print(f"[+] New connection from {client_address[0]}:{client_address[1]}")
    client_socket.settimeout(timeout)

    # client address
    req_ip = client_address[0]
    req_port = client_address[1]

    try:
        # banner
        banner_msg = "Welcome to Ubuntu 20.04.3 TLS\r\n\r\n"
        client_socket.send(banner_msg.encode())

        # start loop
        while True:
            
            # send prompt
            client_socket.send(b"$ ".encode())

            try:

                # data receive
                data = client_socket.recv(1024)

                if not data:
                    print(f"[-] Connection closed by {client_address[0]}:{client_address[1]}")
                    break

                # decode and clean input
                command = data.decode().strip()

                # manage command
                response = process_command(command)

            except socket.timeout:
                print(f"[-] Connection timeout from {client_address[0]}:{client_address[1]}")
                break

    except Exception as e:
        print(f"[-] Exception with {client_address[0]}:{client_address[1]}: {e}")
    finally:
        client_socket.close()
        print(f"[-] Connection closed from {client_address[0]}:{client_address[1]}")

def telnet_server(host=HOST, port=TELNET_PORT, timeout=10):

    #### suggerimento: socket non nella funzione ma nel main

    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, TELNET_PORT))
        server_socket.listen(5)
        print(f"[*] Telnet honeypot listening on {HOST}:{TELNET_PORT}")

        while True:

            try:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, timeout), daemon=True)
                client_thread.start()

            except KeyboardInterrupt:
                print("\n[!] Shutting down server.")
                break
            except Exception as e:
                print(f"[-] Exception: {e}")
    
    finally:
        server_socket.close()
        print("[*] Server socket closed.")

# main
if __name__ == "__main__":
    try:
        telnet_server(HOST, TELNET_PORT, timeout=10)
    except Exception as e:
        print(f"[-] Server error: {e}")
