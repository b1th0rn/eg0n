from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Vuln model: vulnerabilities list 
class Vuln(models.Model):
    cve = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    cvss = models.FloatField(default=0, null=True)
    description = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField()
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)

    def __str__(self):
        return self.cve

# VulnReview model: analysis and docs. 
class VulnReview(models.Model):
    review_name = models.CharField(max_length=64, default="none", unique=True)
    cve_name = models.ForeignKey(Vuln, to_field="name", on_delete=models.CASCADE, default="none", related_name="cve_name")
    review = models.TextField(null=True, blank=True)
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    references_url = models.CharField(max_length=256, null=True, blank=True)
    exploit_url = models.CharField(max_length=256, null=True, blank=True)
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)
    
    def __str__(self):
        return f"Review of {self.cve_name} by {self.lastchange_author}"

# IpAdd model: suspicious IP address list 
CONFIDENCE_CHOICES = [ ('low', 'low'), ('medium', 'medium'), ('high', 'high') ]
class IpAdd(models.Model):
    ip_address = models.GenericIPAddressField(unique=True, unpack_ipv4=True)
    url = models.CharField(max_length=32, blank=True, default='none')
    fqdn = models.CharField(max_length=32, blank=True, default='none')
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    description = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)

    def __str__(self):
        return self.ip_address

# IpAddReview model: analysis and docs.
class IpAddReview(models.Model):
    review_name = models.CharField(max_length=64, default="none", unique=True)
    ip = models.ForeignKey(IpAdd, to_field="ip_address", on_delete=models.CASCADE, default="none", related_name="ip")
    review = models.TextField(null=True, blank=True)
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)

# Hash model: suspicious file hash
CONFIDENCE_CHOICES = [ ('low', 'low'), ('medium', 'medium'), ('high', 'high') ]
PLATFORM = [('Linux', 'Linux'), ('Windows', 'Windows'),('macOS', 'macOS'),]
class Hash(models.Model):
    filename = models.CharField(max_length=56, blank=True, default='none')
    platform = models.CharField(max_length=16, choices=PLATFORM, default='Windows')
    sha256 = models.TextField()
    sha1 = models.TextField()
    md5 = models.TextField()
    website = models.URLField(max_length=50, blank=True, default='none')
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    description = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)

    def __str__(self):
        return self.filename