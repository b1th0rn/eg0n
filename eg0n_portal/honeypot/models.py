from django.db import models

# http honeypot
class http_log(models.Model):
    req_type = models.CharField(max_length=32, unique=False)        # GET, POST, HEAD
    req_path = models.CharField(max_length=256, unique=False)       # path requested
    req_header = models.TextField()
    req_useragent = models.CharField(max_length=256)
    req_xff = models.GenericIPAddressField(unpack_ipv4=True)        # X-Forwarded-For
    log_date = models.DateField(auto_now=False, auto_now_add=True)
    slug = models.SlugField()
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)

