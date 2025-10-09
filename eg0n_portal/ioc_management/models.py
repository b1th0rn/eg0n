from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Vuln model: vulnerabilities list
class Vuln(models.Model):
    class Meta:
        verbose_name = "01 :: Vulnerability"
        verbose_name_plural = "01 :: Vulnerabilities"
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

# IpAdd model: suspicious IP address list
CONFIDENCE_CHOICES = [('low', 'low'), ('medium', 'medium'), ('high', 'high')]
VALIDATION_CHOICES = [('new', 'new'), ('approved', 'approved'), ('sospended', 'sospended')]
class IpAdd(models.Model):
    class Meta:
        verbose_name = "02 :: IP Address"
        verbose_name_plural = "02 :: IP Addresses"
    ip_address = models.GenericIPAddressField(unique=True, unpack_ipv4=True)
    url = models.CharField(max_length=32, blank=True, default='none')
    fqdn = models.CharField(max_length=32, blank=True, default='none')
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    description = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(max_length=32, choices=VALIDATION_CHOICES, default='new')
    misp_attribute_id = models.CharField(max_length=32, blank=True, default='none')
    misp_event_id = models.URLField(max_length=128, blank=True, default='none')
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)
    def __str__(self):
        return self.ip_address

# Code Models: suspicious code
CONFIDENCE_CHOICES = [('low', 'low'), ('medium', 'medium'), ('high', 'high')]
VALIDATION_CHOICES = [('new', 'new'), ('approved', 'approved'), ('sospended', 'sospended')]
Language = [('cmd', 'cmd'), ('powershell', 'powershell'), ('bash', 'bash'), ('python', 'python')]
class CodeSnippet(models.Model):
    class Meta:
        verbose_name = "03 :: Code Snippet"
        verbose_name_plural = "03 :: Code Snippets"
    name = models.CharField(max_length=56, blank=True, default='none', unique=True)
    language = models.CharField(max_length=16, choices=Language, default='python')
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    code = models.TextField()
    description = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(max_length=32, choices=VALIDATION_CHOICES, default='new')
    misp_attribute_id = models.CharField(max_length=32, blank=True, default='none')
    misp_event_id = models.URLField(max_length=128, blank=True, default='none')
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)
    def __str__(self):
        return self.name

# FQDN model: suspicious fqdn lists
CONFIDENCE_CHOICES = [('low', 'low'), ('medium', 'medium'), ('high', 'high')]
VALIDATION_CHOICES = [('new', 'new'), ('approved', 'approved'), ('sospended', 'sospended')]
class FQDN(models.Model):
    class Meta:
        verbose_name = "04 :: FQDN"
        verbose_name_plural = "04 :: FQDNs"
    fqdn = models.CharField(max_length=32, unique=True)
    ip_address = models.GenericIPAddressField(default="0.0.0.0", unpack_ipv4=True)
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    description = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(max_length=32, choices=VALIDATION_CHOICES, default='new')
    misp_attribute_id = models.CharField(max_length=32, blank=True, default='none')
    misp_event_id = models.URLField(max_length=128, blank=True, default='none')
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)
    def __str__(self):
        return self.fqdn

# Hash model: suspicious file hash
CONFIDENCE_CHOICES = [('low', 'low'), ('medium', 'medium'), ('high', 'high')]
PLATFORM = [('Linux', 'Linux'), ('Windows', 'Windows'), ('macOS', 'macOS'), ]
VALIDATION_CHOICES = [('new', 'new'), ('approved', 'approved'), ('sospended', 'sospended')]
class Hash(models.Model):
    class Meta:
        verbose_name = "05 :: File Hash"
        verbose_name_plural = "05 :: File Hashes"
    filename = models.CharField(max_length=56, blank=True, default='none')
    platform = models.CharField(max_length=16, choices=PLATFORM, default='Windows')
    sha256 = models.CharField(max_length=64, blank=True, default='none', unique=True)
    sha1 = models.CharField(max_length=40, blank=True, default='none')
    md5 = models.CharField(max_length=32, blank=True, default='none')
    website = models.URLField(max_length=50, blank=True, default='none.sample')
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    description = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(max_length=32, choices=VALIDATION_CHOICES, default='new')
    misp_attribute_id = models.CharField(max_length=32, blank=True, default='none')
    misp_event_id = models.URLField(max_length=128, blank=True, default='none')
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)
    def __str__(self):
        return "[{}] {}".format(self.filename, self.sha256)

# IoC revirew
class Review(models.Model):
    class Meta:
        verbose_name = "06 :: IoC Review"
        verbose_name_plural = "06 :: IoC Reviews"
    review_name = models.CharField(max_length=64, default="none", unique=True)
    ref_IpAdd = models.ForeignKey(IpAdd, to_field="ip_address", on_delete=models.CASCADE, default="none", related_name="ref_IpAdd", null=True, blank=True)
    ref_FQDN = models.ForeignKey(FQDN, to_field="fqdn", on_delete=models.CASCADE, default="none",related_name="ref_FQDN", null=True, blank=True)
    ref_Hash = models.ForeignKey(Hash, to_field="sha256", on_delete=models.CASCADE, default="none", related_name="ref_Hash", null=True, blank=True)
    ref_CodeSnippet = models.ForeignKey(CodeSnippet, to_field="name", on_delete=models.CASCADE, default="none",related_name="ref_CodeSnippet", null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)
    def __str__(self):
        return self.review_name