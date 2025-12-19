import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


CONFIDENCE_CHOICES = [("low", "low"), ("medium", "medium"), ("high", "high")]
LANGUAGES = [
    ("cmd", "cmd"),
    ("powershell", "powershell"),
    ("bash", "bash"),
    ("python", "python"),
]
PLATFORM = [
    ("linux", "linux"),
    ("windows", "windows"),
    ("macos", "macos"),
]
VALIDATION_CHOICES = [
    ("new", "new"),
    ("approved", "approved"),
    ("suspended", "suspended"),
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
    name = models.CharField(max_length=64, null=False, unique=True)
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
    cve = models.CharField(max_length=32, unique=False)
    cvss = models.FloatField(default=0, null=True)
    description = models.TextField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        default=None,
        related_name="vulns",
        null=True,
    )
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_vulns",
    )
    name = models.CharField(max_length=32, unique=False)
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
        max_length=16, choices=CONFIDENCE_CHOICES, default="low"
    )
    description = models.TextField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        default=None,
        related_name="ipadds",
        null=True,
    )
    expire_date = models.DateField(default=timezone.now)
    fqdn = models.CharField(max_length=32, blank=True, default="none")
    ip_address = models.GenericIPAddressField(unique=False, unpack_ipv4=True)
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_ipadds",
    )
    url = models.CharField(max_length=32, blank=True, default="none")
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
        max_length=16, choices=CONFIDENCE_CHOICES, default="low"
    )
    description = models.TextField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        default=None,
        related_name="codesnippets",
        null=True,
    )
    expire_date = models.DateField(default=timezone.now)
    language = models.CharField(max_length=16, choices=LANGUAGES, default="python")
    name = models.CharField(max_length=56)
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
        max_length=16, choices=CONFIDENCE_CHOICES, default="low"
    )
    description = models.TextField()
    expire_date = models.DateField(default=timezone.now)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, default=None, related_name="fqdns", null=True
    )
    fqdn = models.CharField(max_length=32, unique=False)
    ip_address = models.GenericIPAddressField(default="0.0.0.0", unpack_ipv4=True)
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_fqdns",
    )
    validation_status = models.CharField(
        max_length=32, choices=VALIDATION_CHOICES, default="new"
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
        max_length=16, choices=CONFIDENCE_CHOICES, default="low"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, default=None, related_name="hashes", null=True
    )
    filename = models.CharField(max_length=56, blank=True, default="none")
    contributors_authors = models.ManyToManyField(
        User,
        editable=False,
        related_name="contributed_hashes",
    )
    md5 = models.CharField(max_length=32, blank=True, default="none")
    platform = models.CharField(max_length=16, choices=PLATFORM, default="windows")
    sha1 = models.CharField(max_length=40, blank=True, default="none")
    sha256 = models.CharField(max_length=64, blank=True, default="none", unique=True)
    website = models.URLField(max_length=50, blank=True, default="none.sample")
    description = models.TextField()
    expire_date = models.DateField(default=timezone.now)
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
        Event, on_delete=models.CASCADE, default=None, related_name="reviews", null=True
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
