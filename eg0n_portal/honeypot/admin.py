from django.contrib import admin
from .models import http_log

# Register your models here.

class http_hpAdmin(admin.ModelAdmin):
    list_display = ('req_type', 'req_path', 'req_xff', 'log_date')
    search_fields = ('req_type', 'req_path', 'req_xff')
    list_filter = ('log_date', 'req_xff')
    readonly_fields = ('author', 'lastchange_author')

admin.site.register(http_log, http_hpAdmin)
