import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


#############################################################################
# Instance
#############################################################################


class Instance(models.Model):
    """
    Model for eg0n instances.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "instace"
        ordering = ("name",)
        verbose_name = "Instance Information"
        verbose_name_plural = "Instance Information"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("instance-detail-view", args=[str(self.pk)])


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
        to_field="username",
    )
    description = models.TextField()
    instance = models.ForeignKey(
        Instance, on_delete=models.CASCADE, related_name="events"
    )
    lastchange_author = models.ForeignKey(
        User,
        editable=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="contributed_events",
        to_field="username",
    )
    name = models.CharField(max_length=64, null=False, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
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
        to_field="username",
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
    lastchange_author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contributed_vulns",
        null=True,
    )
    name = models.CharField(max_length=32, unique=False)
    slug = models.SlugField(max_length=128, unique=True)
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


# IpAdd model: suspicious IP address list
CONFIDENCE_CHOICES = [("low", "low"), ("medium", "medium"), ("high", "high")]
VALIDATION_CHOICES = [
    ("new", "new"),
    ("approved", "approved"),
    ("suspended", "suspended"),
]


class IpAdd(models.Model):
    class Meta:
        verbose_name = "02 :: IP Address"
        verbose_name_plural = "02 :: IP Addresses"
        db_table = "ipadds"
        ordering = ["-created"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField(unique=False, unpack_ipv4=True)
    url = models.CharField(max_length=32, blank=True, default="none")
    fqdn = models.CharField(max_length=32, blank=True, default="none")
    confidence = models.CharField(
        max_length=16, choices=CONFIDENCE_CHOICES, default="low"
    )
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(
        max_length=32, choices=VALIDATION_CHOICES, default="new"
    )
    author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="ipadd",
        null=True,
    )
    lastchange_author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contributed_ipadd",
        null=True,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        default=None,
        related_name="ip_address",
        null=True,
    )

    def __str__(self):
        return self.ip_address


# Code Models: suspicious code
CONFIDENCE_CHOICES = [("low", "low"), ("medium", "medium"), ("high", "high")]
VALIDATION_CHOICES = [
    ("new", "new"),
    ("approved", "approved"),
    ("sospended", "sospended"),
]
LANGUAGES = [
    ("cmd", "cmd"),
    ("powershell", "powershell"),
    ("bash", "bash"),
    ("python", "python"),
]


class CodeSnippet(models.Model):
    class Meta:
        verbose_name = "03 :: Code Snippet"
        verbose_name_plural = "03 :: Code Snippets"
        db_table = "codesnippets"
        ordering = ["-created"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=56, blank=True, default="none", unique=True)
    language = models.CharField(max_length=16, choices=LANGUAGES, default="python")
    confidence = models.CharField(
        max_length=16, choices=CONFIDENCE_CHOICES, default="low"
    )
    code = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(
        max_length=32, choices=VALIDATION_CHOICES, default="new"
    )
    author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="codesnippet",
        null=True,
    )
    lastchange_author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contributed_codesnippet",
        null=True,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        default=None,
        related_name="codesnippets",
        null=True,
    )

    def __str__(self):
        return self.name


# FQDN model: suspicious fqdn lists
CONFIDENCE_CHOICES = [("low", "low"), ("medium", "medium"), ("high", "high")]
VALIDATION_CHOICES = [
    ("new", "new"),
    ("approved", "approved"),
    ("sospended", "sospended"),
]


class FQDN(models.Model):
    class Meta:
        verbose_name = "04 :: FQDN"
        verbose_name_plural = "04 :: FQDNs"
        db_table = "FQDNs"
        ordering = ["-created"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fqdn = models.CharField(max_length=32, unique=False)
    ip_address = models.GenericIPAddressField(default="0.0.0.0", unpack_ipv4=True)
    confidence = models.CharField(
        max_length=16, choices=CONFIDENCE_CHOICES, default="low"
    )
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(
        max_length=32, choices=VALIDATION_CHOICES, default="new"
    )
    author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="fqdn",
        null=True,
    )
    lastchange_author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contributed_fqdn",
        null=True,
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, default=None, related_name="FQDNs", null=True
    )

    def __str__(self):
        return self.fqdn


# Hash model: suspicious file hash
CONFIDENCE_CHOICES = [("low", "low"), ("medium", "medium"), ("high", "high")]
PLATFORM = [
    ("Linux", "Linux"),
    ("Windows", "Windows"),
    ("macOS", "macOS"),
]
VALIDATION_CHOICES = [
    ("new", "new"),
    ("approved", "approved"),
    ("sospended", "sospended"),
]


class Hash(models.Model):
    class Meta:
        verbose_name = "05 :: File Hash"
        verbose_name_plural = "05 :: File Hashes"
        db_table = "hashes"
        ordering = ["-created"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=56, blank=True, default="none")
    platform = models.CharField(max_length=16, choices=PLATFORM, default="Windows")
    sha256 = models.CharField(max_length=64, blank=True, default="none", unique=True)
    sha1 = models.CharField(max_length=40, blank=True, default="none")
    md5 = models.CharField(max_length=32, blank=True, default="none")
    website = models.URLField(max_length=50, blank=True, default="none.sample")
    confidence = models.CharField(
        max_length=16, choices=CONFIDENCE_CHOICES, default="low"
    )
    description = models.TextField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    expire_date = models.DateField(default=timezone.now)
    validation_status = models.CharField(
        max_length=32, choices=VALIDATION_CHOICES, default="new"
    )
    author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="hash",
        null=True,
    )
    lastchange_author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contributed_hash",
        null=True,
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, default=None, related_name="hashes", null=True
    )

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
    author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="review",
        null=True,
    )
    lastchange_author = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contributed_review",
        null=True,
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, default=None, related_name="reviews", null=True
    )

    def __str__(self):
        return "[{}] {}".format(self.event, self.name)
