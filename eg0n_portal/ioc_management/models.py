from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Instance
class Instance(models.Model):
    class Meta:
        verbose_name = "Instance Information"
        verbose_name_plural = "Instance Information"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

# Threat Int. events
class Event(models.Model):
    class Meta:
        verbose_name = "00 :: Event"
        verbose_name_plural = "00 :: Events"
        db_table = "events"
        ordering = ["-created"]
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, related_name="events")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False, unique=True)
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="events", null=True)
    lastchange_author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="contributed_events", null=True)
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name

# Vuln model: vulnerabilities list
class Vuln(models.Model):
    class Meta:
        verbose_name = "01 :: Vulnerability"
        verbose_name_plural = "01 :: Vulnerabilities"
        db_table = "vulns"
        ordering = ["-created"]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cve = models.CharField(max_length=32, unique=False)
    name = models.CharField(max_length=32, unique=False)
    cvss = models.FloatField(default=0, null=True)
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="vulns", null=True)
    lastchange_author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="contributed_vulns", null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, related_name="vuln", null=True)
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.cve

# IpAdd model: suspicious IP address list
CONFIDENCE_CHOICES = [('low', 'low'), ('medium', 'medium'), ('high', 'high')]
VALIDATION_CHOICES = [('new', 'new'), ('approved', 'approved'), ('suspended', 'suspended')]
class IpAdd(models.Model):
    class Meta:
        verbose_name = "02 :: IP Address"
        verbose_name_plural = "02 :: IP Addresses"
        db_table = "ipadds"
        ordering = ["-created"]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField(unique=False, unpack_ipv4=True)
    url = models.CharField(max_length=32, blank=True, default='none')
    fqdn = models.CharField(max_length=32, blank=True, default='none')
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(max_length=32, choices=VALIDATION_CHOICES, default='new')
    author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="ipadd", null=True)
    lastchange_author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="contributed_ipadd", null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, related_name="ip_address", null=True)
    
    def __str__(self):
        return self.ip_address

# Code Models: suspicious code
CONFIDENCE_CHOICES = [('low', 'low'), ('medium', 'medium'), ('high', 'high')]
VALIDATION_CHOICES = [('new', 'new'), ('approved', 'approved'), ('sospended', 'sospended')]
LANGUAGES = [('cmd', 'cmd'), ('powershell', 'powershell'), ('bash', 'bash'), ('python', 'python')]
class CodeSnippet(models.Model):
    class Meta:
        verbose_name = "03 :: Code Snippet"
        verbose_name_plural = "03 :: Code Snippets"
        db_table = "codesnippets"
        ordering = ["-created"]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=56, blank=True, default='none', unique=True)
    language = models.CharField(max_length=16, choices=LANGUAGES, default='python')
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    code = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(max_length=32, choices=VALIDATION_CHOICES, default='new')
    author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="codesnippet", null=True)
    lastchange_author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="contributed_codesnippet", null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, related_name="codesnippets", null=True)
    
    def __str__(self):
        return self.name

# FQDN model: suspicious fqdn lists
CONFIDENCE_CHOICES = [('low', 'low'), ('medium', 'medium'), ('high', 'high')]
VALIDATION_CHOICES = [('new', 'new'), ('approved', 'approved'), ('sospended', 'sospended')]
class FQDN(models.Model):
    class Meta:
        verbose_name = "04 :: FQDN"
        verbose_name_plural = "04 :: FQDNs"
        db_table = "FQDNs"
        ordering = ["-created"]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fqdn = models.CharField(max_length=32, unique=False)
    ip_address = models.GenericIPAddressField(default="0.0.0.0", unpack_ipv4=True)
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(max_length=32, choices=VALIDATION_CHOICES, default='new')
    author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="fqdn", null=True)
    lastchange_author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="contributed_fqdn", null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, related_name="FQDNs", null=True)

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
        db_table = "hashes"
        ordering = ["-created"]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=56, blank=True, default='none')
    platform = models.CharField(max_length=16, choices=PLATFORM, default='Windows')
    sha256 = models.CharField(max_length=64, blank=True, default='none', unique=True)
    sha1 = models.CharField(max_length=40, blank=True, default='none')
    md5 = models.CharField(max_length=32, blank=True, default='none')
    website = models.URLField(max_length=50, blank=True, default='none.sample')
    confidence = models.CharField(max_length=16, choices=CONFIDENCE_CHOICES, default='low')
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(max_length=32, choices=VALIDATION_CHOICES, default='new')
    author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="hash", null=True)
    lastchange_author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="contributed_hash", null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, related_name="hashes", null=True)

    def __str__(self):
        return "[{}] {}".format(self.filename, self.sha256)

# IoC revirew
class Review(models.Model):
    class Meta:
        verbose_name = "06 :: IoC Review"
        verbose_name_plural = "06 :: IoC Reviews"
        db_table = "reviews"
        ordering = ["-created"]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, default="none", unique=True)
    review = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="review", null=True)
    lastchange_author = models.ForeignKey(User, to_field="username", on_delete=models.SET_NULL, editable=False, related_name="contributed_review", null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, related_name="reviews", null=True)

    def __str__(self):
        return "[{}] {}".format(self.event, self.name)