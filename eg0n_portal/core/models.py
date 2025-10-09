from django.db import models

# base api configuration
class apiConfig(models.Model):
    class Meta:
        verbose_name = "00 :: API Configuration"
        verbose_name_plural = "00 :: API Configurations"
    api_name = models.CharField(max_length=32, unique=True)
    api_url = models.CharField(max_length=128)
    api_key = models.CharField(max_length=128)
    api_verify_cert = models.BooleanField(default=True)
    api_timeout = models.IntegerField(default=10)
    api_description = models.TextField()
    def __str__(self):
        return self.api_name
