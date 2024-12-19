from django.contrib import admin
from .models import Vuln, VulnReview, ipadd, hash

# Vulnerabilities: custom admin
class VulnsAdmin(admin.ModelAdmin):
    list_display = ["name", "cve", "cvss", "publish_date", "lastchange_author"]
    list_filter = ["publish_date"]
    search_fields = ["name", "name"]
    prepopulated_fields = {"slug": ("name",)}
    # author field
    readonly_fields = ("author", "lastchange_author")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = Vuln

class VulnReviewAdmin(admin.ModelAdmin):
    # admin view
    list_display = ["cve", "publish_date", "author", "author"]
    list_filter = ["publish_date"]
    search_fields = ["cve", "author"]
    # author field
    readonly_fields = ("author", "lastchange_author")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = VulnReview

# IP Address: custom admin
class IpAdmin(admin.ModelAdmin):
    list_display = ["ip_address", "url", "fqdn", "publish_date", "expire_date", "lastchange_author"]
    list_filter = ["publish_date"]
    search_fields = ["ip_address", "url"]
    # author field
    readonly_fields = ("author", "lastchange_author")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = ipadd

# Hashes: custom admin 
class HashAdmin(admin.ModelAdmin):
    list_display = ["filename", "platform", "website", "sha256", "sha1", "md5", "publish_date", "expire_date", "lastchange_author"]
    list_filter = ["publish_date"]
    search_fields = ["sha256", "sha1","md5"]
    # author field
    readonly_fields = ("author", "lastchange_author")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = hash


# Register
admin.site.register(Vuln, VulnsAdmin)
admin.site.register(VulnReview, VulnReviewAdmin)
admin.site.register(ipadd, IpAdmin)
admin.site.register(hash, HashAdmin)