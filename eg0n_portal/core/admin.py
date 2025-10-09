from django.contrib import admin
from .models import apiConfig

class apiConfigAdmin(admin.ModelAdmin):
    list_display = ["api_name", "api_url", "api_description"]
    search_fields = ["api_name", "api_url"]
    class Meta:
        model = apiConfig

admin.site.register(apiConfig, apiConfigAdmin)