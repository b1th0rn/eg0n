from django.contrib import admin
from .models import Vuln, VulnReview, IpAdd, IpAddReview, Hash, HashReview, CodeSnippet, CodeReview
import random

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
    list_display = ["review_name", "cve_name", "publish_date", "author"]
    list_filter = ["publish_date"]
    search_fields = ["cve_name", "author"]
    # author field
    readonly_fields = ("author", "lastchange_author", "review_name")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
            obj.review_name = "{}_Rev{}".format(obj.cve_name, random.randint(100, 999))
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = VulnReview

# CodeSnippet: custom admin
class CodeAdmin(admin.ModelAdmin):
    list_display = ["name", "language", "publish_date", "lastchange_author"]
    list_filter = ["publish_date"]
    search_fields = ["name", "language"]
    # author field
    readonly_fields = ("author", "lastchange_author")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = CodeSnippet

class CodeReviewAdmin(admin.ModelAdmin):
    # admin view
    list_display = ["review_name", "code_review", "publish_date", "author"]
    list_filter = ["publish_date"]
    search_fields = ["review_name", "author"]
    # author field
    readonly_fields = ("author", "lastchange_author", "review_name")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
            obj.review_name = "{}_Rev{}".format(obj.code_review, random.randint(100, 999))
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = CodeReview

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
        model = IpAdd

class IpAddReviewAdmin(admin.ModelAdmin):
    # admin view
    list_display = ["review_name", "ip", "publish_date", "author"]
    list_filter = ["publish_date"]
    search_fields = ["ip", "author"]
    # author field
    readonly_fields = ("author", "lastchange_author", "review_name")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
            obj.review_name = "{}_Rev{}".format(obj.ip, random.randint(100, 999))
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = IpAddReview

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
        model = Hash

class HashReviewAdmin(admin.ModelAdmin):
    # admin view
    list_display = ["review_name", "hash", "publish_date", "author"]
    list_filter = ["publish_date"]
    search_fields = ["hash", "author"]
    # author field
    readonly_fields = ("author", "lastchange_author", "review_name")
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
            obj.review_name = "{}_Rev{}".format(obj.hash, random.randint(100, 999))
        obj.lastchange_author = request.user.username
        return super().save_model(request, obj, form, change)
    class Meta:
        model = HashReview

# Register
admin.site.register(Vuln, VulnsAdmin)
admin.site.register(VulnReview, VulnReviewAdmin)

admin.site.register(IpAdd, IpAdmin)
admin.site.register(IpAddReview, IpAddReviewAdmin)

admin.site.register(Hash, HashAdmin)
admin.site.register(HashReview, HashReviewAdmin)

admin.site.register(CodeSnippet, CodeAdmin )
admin.site.register(CodeReview, CodeReviewAdmin)