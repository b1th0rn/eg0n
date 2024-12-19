from django.db import models
from django.contrib.auth.models import User
from info_gathering.models import OrganizationInfo, PersonInfo
from ioc_management.models import VulnReview
from datetime import datetime, timezone

# Asset Models
class Asset(models.Model):
    NETWORK_ZONE_LIST = [ ('client', 'client'), ('server', 'server'), ('dmz', 'dmz'), ('public', 'public') ]
    IMPACT_LEVEL = [ ('low', 'low'), ('medium', 'medium'), ('high', 'high') ]
    YES_NO = [ ('yes', 'yes'), ('no', 'no') ]
    organization = models.ForeignKey(OrganizationInfo, to_field="organization_name", on_delete=models.CASCADE, db_column="organization_name")
    owner = models.ForeignKey(PersonInfo, to_field="name", on_delete=models.CASCADE, db_column="name")
    hostname = models.CharField(max_length=32, unique=True)
    ipadd = models.CharField(max_length=32)
    network_zone = models.CharField(max_length=16, choices=NETWORK_ZONE_LIST)
    behind_utm_firewall = models.CharField(max_length=16, choices=YES_NO)
    edr_active = models.CharField(max_length=16, choices=YES_NO)
    soc_scope = models.CharField(max_length=16, choices=YES_NO)
    sensitive_data = models.CharField(max_length=16, choices=YES_NO)
    business_impact = models.CharField(max_length=16, choices=IMPACT_LEVEL)
    end_of_life = models.DateField(default=datetime.now(timezone.utc))
    description = models.TextField()
    
    def __str__(self):
        return self.cve

class CriticalVuln(models.Model):
    asset = models.ForeignKey(Asset, to_field="hostname", on_delete=models.CASCADE, db_column="hostname")
    cve = models.ForeignKey(VulnReview, to_field="cve", on_delete=models.CASCADE, db_column="cve")
    owner = models.ForeignKey(PersonInfo, to_field="name", on_delete=models.CASCADE, db_column="name")