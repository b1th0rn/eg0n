from django.db import models

# base configuration model
class BaseConfig(models.Model):
    class Meta:
        verbose_name = "00 :: Base Configuration"
        verbose_name_plural = "00 :: Base Configurations"
    param_name = models.CharField(max_length=32, unique=True)
    param_value = models.CharField(max_length=128)
    param_description = models.TextField()
    create_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    author = models.CharField(max_length=32, editable=False, default=None)
    lastchange_author = models.CharField(max_length=32, editable=False, default=None)
    def __str__(self):
        return self.param_name

# base api configuration
class apiConfig(models.Model):
    class Meta:
        verbose_name = "01 :: API Configuration"
        verbose_name_plural = "01 :: API Configurations"
    api_name = models.CharField(max_length=32, unique=True)
    api_url = models.CharField(max_length=128)
    api_key = models.CharField(max_length=128)
    api_verify_cert = models.BooleanField(default=True)
    api_timeout = models.IntegerField(default=10)
    api_description = models.TextField()
    def __str__(self):
        return self.api_name
