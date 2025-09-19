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

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
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

        # salvataggio in django
        http_log.objects.create(
            req_type=req_type,
            req_path=req_path,
            req_header=req_header,
            req_useragent=user_agent,
            req_xff=xff,
            log_date=timezone.now().date(),
            slug='http-honeypot-log',
            author='honeypot',
            lastchange_author='honeypot'
        )
