from django.db import models

# base api configuration
class apiConfig(models.Model):
    api_name = models.CharField(max_length=32, unique=True)
    api_url = models.CharField(max_length=128)
    api_key = models.CharField(max_length=128)
    api_description = models.TextField()
    def __str__(self):
        return self.api_name
