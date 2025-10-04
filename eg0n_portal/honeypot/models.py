from django.db import models

# http honeypot
class http_log(models.Model):
    class Meta:
        verbose_name = "01 :: HTTP Honeypot"
        verbose_name_plural = "01 :: HTTP Honeypot"
    req_type = models.CharField(max_length=32, unique=False)        # GET, POST, HEAD
    req_path = models.CharField(max_length=256, unique=False)       # path requested
    req_header = models.TextField(blank=True, default='none')       # full header
    req_body = models.TextField(blank=True, default='none')
    req_useragent = models.CharField(max_length=256)
    req_xff = models.GenericIPAddressField(unpack_ipv4=True)        # X-Forwarded-For
    log_date = models.DateField(auto_now=False, auto_now_add=True)
    slug = models.SlugField()
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)

# telnet honeypot
class telnet_log(models.Model):
    class Meta:
        verbose_name = "02 :: Telnet Honeypot"
        verbose_name_plural = "02 :: Telnet Honeypot"
    req_ip = models.GenericIPAddressField(unpack_ipv4=True)         # IP address
    req_port = models.IntegerField()                                # Port
    req_username = models.CharField(max_length=64, unique=False)    # username
    req_password = models.CharField(max_length=64, unique=False)    # password
    req_command = models.TextField(blank=True, default='none')      # command executed
    log_date = models.DateField(auto_now=False, auto_now_add=True)
    slug = models.SlugField()
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)   