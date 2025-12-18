from django.contrib import admin
from .models import Event, Vuln, IpAdd, FQDN, Hash, CodeSnippet, Review, Instance
from django.utils.html import format_html
import random

# == VULNS INLINE FOR EVENTS ADMIN ==
class VulnsInline(admin.TabularInline):
    model = Vuln
    extra = 0
    fields = ("cve", "cvss", "description")
    readonly_fields = ("cve", "cvss", "description")
    show_change_link = True

# == IPADD INLINE FOR EVENTS ADMIN ==
class IpAddInline(admin.TabularInline):
    model = IpAdd
    extra = 0
    fields = ("ip_address", "confidence", "description")
    readonly_fields = ("ip_address", "confidence", "description")
    show_change_link = True

# == INSTANCE ADMIN ==
class InstanceAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    class Meta:
        model = Instance

# E== EVENTS ADMIN ==
class EventsAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "author", "lastchange_author"]
    list_filter = ["created_at"]
    search_fields = ["name", "author"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("author", "lastchange_author")
    inlines = [VulnsInline, IpAddInline]

    class Meta:
        model = Vuln

    # == override save model to set author and lastchange_author ==
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.lastchange_author = request.user
        return super().save_model(request, obj, form, change)

# == VULNS ADMIN ==
class VulnsAdmin(admin.ModelAdmin):
    list_display = ["name", "cve", "cvss", "created_at", "lastchange_author"]
    list_filter = ["created_at"]
    search_fields = ["name", "name"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("author", "lastchange_author")

    class Meta:
        model = Vuln

    # == override save model to set author and lastchange_author ==
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.lastchange_author = request.user
        super().save_model(request, obj, form, change)

# == IPADD ADMIN ==
class IpAdmin(admin.ModelAdmin):
    list_display = ["ip_address", "url", "created", "expire_date", "lastchange_author"]
    list_filter = ["created"]
    search_fields = ["ip_address", "url"]
    readonly_fields = ("author", "lastchange_author")

    class Meta:
        model = Vuln

    # == override save model to set author and lastchange_author ==
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.lastchange_author = request.user
        super().save_model(request, obj, form, change)

# == CODESNIPPET ADMIN ==
class CodeAdmin(admin.ModelAdmin):
    list_display = ["name", "language", "created", "lastchange_author"]
    list_filter = ["created"]
    search_fields = ["name", "language"]
    readonly_fields = ("author", "lastchange_author")

    class Meta:
        model = Vuln

    # == override save model to set author and lastchange_author ==
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.lastchange_author = request.user
        super().save_model(request, obj, form, change)

# == FQDN ADMIN ==
class FQDNAdmin(admin.ModelAdmin):
    list_display = ["fqdn", "created", "expire_date", "lastchange_author"]
    list_filter = ["created"]
    search_fields = ["fqdn"]
    readonly_fields = ("author", "lastchange_author")

    class Meta:
        model = Vuln

    # == override save model to set author and lastchange_author ==
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.lastchange_author = request.user
        super().save_model(request, obj, form, change)

# == HASH ADMIN ==
class HashAdmin(admin.ModelAdmin):
    list_display = ["filename", "platform", "sha256", "expire_date", "lastchange_author"]
    list_filter = ["created"]
    search_fields = ["sha256", "sha1", "md5"]
    readonly_fields = ("author", "lastchange_author")

    class Meta:
        model = Vuln

    # == override save model to set author and lastchange_author ==
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.lastchange_author = request.user
        super().save_model(request, obj, form, change)

# == REVIEW ADMIN ==
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "author"]
    list_filter = ["created"]
    search_fields = ["name", "author"]
    readonly_fields = ("author", "lastchange_author")

    class Meta:
        model = Vuln

    # == override save model to set author and lastchange_author ==
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.lastchange_author = request.user
        super().save_model(request, obj, form, change)
        return super().save_model(request, obj, form, change)

# == REGISTER MODELS TO ADMIN SITE ==
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Event, EventsAdmin)
admin.site.register(Vuln, VulnsAdmin)
admin.site.register(IpAdd, IpAdmin)
admin.site.register(FQDN, FQDNAdmin)
admin.site.register(Hash, HashAdmin)
admin.site.register(CodeSnippet, CodeAdmin )
admin.site.register(Review, ReviewAdmin)
