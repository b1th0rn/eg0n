import os, sys, socket, datetime, json, random

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

# clean input
def clean_input(data):
    ### clean IAC
    cleaned = b''
    i = 0
    while i < len(data):
        if data[i:i+1] == b'\xff':
            i+=3
        else:
            cleaned += data[i:i+1]
            i+=1
    return cleaned.decode('utf-8', errors='ignore')

# telnet server
def telnet_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, TELNET_PORT))
    server_socket.listen(5)
    print(f"[*] Telnet honeypot listening on {HOST}:{TELNET_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_socket.send(BANNER.encode('utf-8'))

        # richiesta username
        client_socket.send(b"login: ")
        raw_username = client_socket.recv(1024)
        req_username = clean_input(raw_username)
        add_log(addr[0], addr[1], req_username, 'none', 'Login Attempt')
        client_socket.send(b"Password: ")
        
        # richiesta password
        req_password = client_socket.recv(1024).decode('utf-8').strip()
        add_log(addr[0], addr[1], req_username, req_password, 'Password Attempt')
        client_socket.send(b"\r\nWelcome to Ubuntu!\r\n$ ")

        # richiesta comandi
        while True:
            req_command = client_socket.recv(1024).decode('utf-8').strip()
            if req_command.lower() in ['exit', 'quit']:
                client_socket.send(b"Logout\r\n")
                break
            response = f"bash: {req_command}: command not found\r\n$ "
            client_socket.send(response.encode('utf-8'))

            # salvataggio log su DB
            add_log(addr[0], addr[1], req_username, req_password, req_command)

        client_socket.close()
        print(f"[*] Closed connection from {addr[0]}:{addr[1]}")

# funziona mail
if __name__ == "__main__":
    try:
        telnet_server()
    except KeyboardInterrupt:
        print("\n[*] Shutting down the server.")
        sys.exit(0)