"""Define ORM models for IoC Management app."""

import uuid
from datetime import timedelta
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


DEFAULT_MAX_LENGTH = 64
def DEFAULT_EXPIRED_AT():
    return timezone.now() + timedelta(days=30)
CONFIDENCE_CHOICES = [("low", "low"), ("medium", "medium"), ("high", "high")]
LANGUAGES = [
    ("bash", "Bash"),
    ("cmd", "CMD"),
    ("powershell", "PowerShell"),
    ("python", "Python"),
]
PLATFORM = [
    ("linux", "Linux"),
    ("macos", "MacOS"),
    ("windows", "Windows"),
]
VALIDATION_CHOICES = [
    ("new", "New"),
    ("approved", "Approved"),
    ("suspended", "Suspended"),
]


#############################################################################
# Event
#############################################################################


class Event(models.Model):
    """
    Model for Threat Intelligence events.
    """

    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    author = models.ForeignKey(
        User,
        editable=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="events",
    )
    description = models.TextField()
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_events",
    )
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "event"
        ordering = ("-created_at",)
        verbose_name = "00 :: Event"
        verbose_name_plural = "00 :: Events"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("event-detail-view", args=[str(self.pk)])


#############################################################################
# CodeSnippet
#############################################################################


class CodeSnippet(models.Model):
    """
    Model for code snippets.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="codesnippets",
        null=True,
    )
    code = models.TextField()
    confidence = models.CharField(
        max_length=DEFAULT_MAX_LENGTH, choices=CONFIDENCE_CHOICES, default="low"
    )
    description = models.TextField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="codesnippets",
    )
    expired_at = models.DateTimeField(default=DEFAULT_EXPIRED_AT)
    language = models.CharField(max_length=DEFAULT_MAX_LENGTH, choices=LANGUAGES, default="python")
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_codesnippets",
    )
    validation_status = models.CharField(
        max_length=32, choices=VALIDATION_CHOICES, default="new"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        verbose_name = "03 :: Code Snippet"
        verbose_name_plural = "03 :: Code Snippets"
        db_table = "codesnippet"
        ordering = ("-created_at",)

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("codesnippet-detail-view", args=[str(self.pk)])


#############################################################################
# Exploit
#############################################################################


class Exploit(models.Model):
    """
    Model for exploits and payloads.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="exploits",
        null=True,
    )
    # associate exploit to EVENT
    event = models.ForeignKey(
        "Event",
        on_delete=models.CASCADE,
        related_name="exploits",
    )
    # associate exploit to VULN
    vuln = models.ForeignKey(
        "Vuln",
        on_delete=models.CASCADE,
        editable=False,
        related_name="exploits",
    )
    description = models.TextField()
    payload = models.TextField()
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_exploits",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        verbose_name = "07 :: Exploit"
        verbose_name_plural = "07 :: Exploits"
        db_table = "exploits"
        ordering = ("-updated_at",)

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("exploit-detail-view", args=[str(self.pk)])
    

#############################################################################
# FQDN
#############################################################################


class FQDN(models.Model):
    """
    Model for FQDNs.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="fqdns",
        null=True,
    )
    confidence = models.CharField(
        max_length=DEFAULT_MAX_LENGTH, choices=CONFIDENCE_CHOICES, default="low"
    )
    description = models.TextField()
    expired_at = models.DateTimeField(default=DEFAULT_EXPIRED_AT)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="fqdns",
    )
    fqdn = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_fqdns",
    )
    validation_status = models.CharField(
        max_length=DEFAULT_MAX_LENGTH, choices=VALIDATION_CHOICES, default="new"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        verbose_name = "04 :: FQDN"
        verbose_name_plural = "04 :: FQDNs"
        db_table = "fqdn"
        ordering = ("-created_at",)

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.fqdn

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("fqdn-detail-view", args=[str(self.pk)])


#############################################################################
# Hash
#############################################################################


class Hash(models.Model):
    """
    Model for file hashes.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="hashes",
        null=True,
    )
    confidence = models.CharField(
        max_length=DEFAULT_MAX_LENGTH, choices=CONFIDENCE_CHOICES, default="low"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="hashes",
    )
    filename = models.CharField(max_length=DEFAULT_MAX_LENGTH, null=True, blank=True)
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_hashes",
    )
    md5 = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True, null=True)
    platform = models.CharField(max_length=DEFAULT_MAX_LENGTH, choices=PLATFORM, default="windows")
    sha1 = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True, null=True)
    sha256 = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True, null=True)
    url = models.URLField(max_length=DEFAULT_MAX_LENGTH, blank=True, null=True)
    description = models.TextField()
    expired_at = models.DateTimeField(default=DEFAULT_EXPIRED_AT)
    validation_status = models.CharField(
        max_length=32, choices=VALIDATION_CHOICES, default="new"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        verbose_name = "05 :: File Hash"
        verbose_name_plural = "05 :: File Hashes"
        db_table = "hashes"
        ordering = ("-created_at",)

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return "[{}] {}".format(self.filename, self.sha256)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("hash-detail-view", args=[str(self.pk)])


#############################################################################
# IpAdd
#############################################################################


class IpAdd(models.Model):
    """
    Model for IP addresses.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="ipadds",
        null=True,
    )
    confidence = models.CharField(
        max_length=DEFAULT_MAX_LENGTH, choices=CONFIDENCE_CHOICES, default="low"
    )
    description = models.TextField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="ipadds",
    )
    expired_at = models.DateTimeField(default=DEFAULT_EXPIRED_AT)
    ip_address = models.GenericIPAddressField(unique=False, unpack_ipv4=True)
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_ipadds",
    )
    validation_status = models.CharField(
        max_length=32, choices=VALIDATION_CHOICES, default="new"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "ipadd"
        ordering = ("-created_at",)
        verbose_name = "02 :: IP Address"
        verbose_name_plural = "02 :: IP Addresses"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.ip_address

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("ipadd-detail-view", args=[str(self.pk)])


#############################################################################
# Review
#############################################################################


class Review(models.Model):
    """
    Model for IoC reviews.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="reviews",
        null=True,
    )
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_reviews",
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="reviews",
    )
    name = models.CharField(max_length=64, default="none", unique=True)
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        verbose_name = "06 :: IoC Review"
        verbose_name_plural = "06 :: IoC Reviews"
        db_table = "reviews"
        ordering = ("-created_at",)

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return "[{}] {}".format(self.event, self.name)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("review-detail-view", args=[str(self.pk)])


#############################################################################
# Vuln
#############################################################################


class Vuln(models.Model):
    """
    Model for vulnerabilities.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="vulns",
        null=True,
    )
    cve = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    cvss = models.FloatField()
    description = models.TextField()
    exploitation_details = models.TextField(blank=True, null=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="vulns",
    )
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_vulns",
    )
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        verbose_name = "01 :: Vulnerability"
        verbose_name_plural = "01 :: Vulnerabilities"
        db_table = "vuln"
        ordering = ("-created_at",)

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("vuln-detail-view", args=[str(self.pk)])
