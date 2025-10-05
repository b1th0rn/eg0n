import os, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eg0n_portal.settings")
import django
django.setup()

from http.server import BaseHTTPRequestHandler, HTTPServer
from honeypot.models import http_log
from django.utils import timezone

# funzione di scrittura del log
def add_log(req_type, req_path, req_header, req_body, req_useragent, req_xff):
    http_log.objects.create(
        req_type=req_type,
        req_path=req_path,
        req_header=req_header,
        req_body=req_body,
        req_useragent=req_useragent,
        req_xff=req_xff,
        log_date=timezone.now().date(),
        slug='http-honeypot-log',
        author='honeypot',
        lastchange_author='honeypot'
    )

# pagina di login
def login_page():
    try:
        with open("http_honeypot_login.html", "r") as file:
            html = file.read()
        return html
    except FileNotFoundError:
        pass

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        # gestione richiesta
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Server is running')

            # definizione variabili per il log
            req_type = self.command
            req_path = self.path
            user_agent = self.headers.get('User-Agent', 'unknown')
            xff = self.headers.get('X-Forwarded-For', self.client_address[0])
            req_header = str(self.headers)

            # salvataggio in django
            add_log(req_type, req_path, req_header, 'none', user_agent, xff)
        elif self.path == '/login':
            self.send_response(200)
            self.end_headers()
            html = login_page()
            self.wfile.write(html.encode('utf-8'))

            # definizione variabili per il log
            req_type = self.command
            req_path = self.path
            user_agent = self.headers.get('User-Agent', 'unknown')
            xff = self.headers.get('X-Forwarded-For', self.client_address[0])
            req_header = str(self.headers)

            # salvataggio in django
            add_log(req_type, req_path, req_header, 'none', user_agent, xff)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

            # definizione variabili per il log
            req_type = self.command
            req_path = self.path
            user_agent = self.headers.get('User-Agent', 'unknown')
            xff = self.headers.get('X-Forwarded-For', self.client_address[0])
            req_header = str(self.headers)

            # salvataggio in django
            add_log(req_type, req_path, req_header, 'none', user_agent, xff)

    def do_POST(self):
        # gestione richiesta
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Server is running')

        # definizione variabili per il log
        req_type = self.command
        req_path = self.path
        user_agent = self.headers.get('User-Agent', 'unknown')
        xff = self.headers.get('X-Forwarded-For', self.client_address[0])
        req_header = str(self.headers)
        req_body = self.rfile.read(int(self.headers.get('Content-Length', 0)))

        # salvataggio in django
        add_log(req_type, req_path, req_header, req_body.decode('utf-8', errors='ignore'), user_agent, xff)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('127.0.0.1', 8888) 
    httpd = server_class(server_address, handler_class)
    print('Starting http honeypot server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()