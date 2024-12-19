from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone

# Organizations
class OrganizationInfo(models.Model):
    organization_name = models.CharField(max_length=64, unique=True)
    organization_address = models.CharField(max_length=64, blank=True, default='none')
    organization_coordinates = models.CharField(max_length=64, blank=True, default='none')
    url = models.CharField(max_length=64, blank=True, default='none')
    description = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.organization_name

class PersonInfo(models.Model):
    name = models.CharField(max_length=64, unique=True)
    address = models.CharField(max_length=64, blank=True, default='none')
    coordinates = models.CharField(max_length=64, blank=True, default='none')
    email = models.CharField(max_length=64, blank=True, default='none')
    mobile = models.CharField(max_length=64, blank=True, default='none')
    website = models.CharField(max_length=64, blank=True, default='none')
    linkedin = models.CharField(max_length=64, blank=True, default='none')
    facebook = models.CharField(max_length=64, blank=True, default='none')
    instagram = models.CharField(max_length=64, blank=True, default='none')
    tiktok = models.CharField(max_length=64, blank=True, default='none')
    mastodon = models.CharField(max_length=64, blank=True, default='none')
    description = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

class DomainName(models.Model):
    domain_name = models.CharField(max_length=64, unique=True)
    organization_name = models.ForeignKey(OrganizationInfo, to_field="organization_name", on_delete=models.CASCADE, db_column="organization_name", default="none", null=True)
    administrative_contact = models.ForeignKey(PersonInfo, to_field="name", on_delete=models.CASCADE, default="none", related_name="administrative")
    technical_contact = models.ForeignKey(PersonInfo, to_field="name", on_delete=models.CASCADE, default="none", related_name="technical")
    name_server_1 = models.CharField(max_length=64, blank=True, default='none')
    name_server_2 = models.CharField(max_length=64, blank=True, default='none')
    name_server_3 = models.CharField(max_length=64, blank=True, default='none')
    description = models.TextField()
    create_date = models.DateField(default=datetime.now(timezone.utc))
    update_date = models.DateField(default=datetime.now(timezone.utc))
    expire_date = models.DateField(default=datetime.now(timezone.utc))

    def __str__(self):
        return self.domain_name
