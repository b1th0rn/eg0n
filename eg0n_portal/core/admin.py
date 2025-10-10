from django.contrib import admin
from .models import apiConfig, BaseConfig

class BaseConfigAdmin(admin.ModelAdmin):
    list_display = ["param_name", "param_value", "param_description"]
    search_fields = ["param_name", "param_value", "param_description"]
    readonly_fields = ("author", "lastchange_author")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = BaseConfig

class apiConfigAdmin(admin.ModelAdmin):
    list_display = ["api_name", "api_url", "api_description"]
    search_fields = ["api_name", "api_url"]
    readonly_fields = ("author", "lastchange_author")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = apiConfig

admin.site.register(BaseConfig, BaseConfigAdmin)
admin.site.register(apiConfig, apiConfigAdmin)