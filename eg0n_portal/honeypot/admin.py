from django.contrib import admin
from .models import HttpLog, TelnetLog

# Register your models here.

class HttpLogAdmin(admin.ModelAdmin):
    list_display = ('req_type', 'req_path', 'req_xff', 'log_date')
    search_fields = ('req_type', 'req_path', 'req_xff')
    list_filter = ('log_date', 'req_xff')
    readonly_fields = ('author', 'lastchange_author')

class TelnetLogAdmin(admin.ModelAdmin):
    list_display = ('req_ip', 'req_port', 'req_username', 'req_command', 'log_date')
    search_fields = ('req_ip', 'req_username', 'req_command')
    list_filter = ('log_date', 'req_ip')
    readonly_fields = ('author', 'lastchange_author')

admin.site.register(HttpLog, HttpLogAdmin)
admin.site.register(TelnetLog, TelnetLogAdmin)
