from django.contrib import admin
from .models import Event, Vuln, IpAdd, FQDN, Hash, CodeSnippet, Review, Exploit
from django.utils.html import format_html
import random

# == VULNS INLINE FOR EVENTS ADMIN ==
class VulnsInline(admin.TabularInline):
    model = Vuln
    extra = 0
    fields = ("cve", "cvss", "description")
    # readonly_fields = ("cve", "cvss", "description")
    show_change_link = True

# == IPADD INLINE FOR EVENTS ADMIN ==
class IpAddInline(admin.TabularInline):
    model = IpAdd
    extra = 0
    fields = ("ip_address", "confidence", "description")
    # readonly_fields = ("ip_address", "confidence", "description")
    show_change_link = True

# == FQDN INLINE FOR EVENTS ADMIN ==
class FQDNInLine(admin.TabularInline):
    model = FQDN
    extra = 0
    fields = ("fqdn", "confidence", "description")
    # readonly_fields = ("fqdn", "confidence", "description")
    show_change_link = True

# == HASH INLINE FOR EVENTS ADMIN ==
class HashInLine(admin.TabularInline):
    model = Hash
    extra = 0
    fields = ("filename", "confidence", "description")
    # readonly_fields = ("filename", "confidence", "description")
    show_change_link = True

# == CodeSnippet INLINE FOR EVENTS ADMIN ==
class CodeSnippetInLine(admin.TabularInline):
    model = CodeSnippet
    extra = 0
    fields = ("name", "confidence", "description")
    # readonly_fields = ("name", "confidence", "description")
    show_change_link = True

# == Review INLINE FOR EVENTS ADMIN ==
class ReviewInLine(admin.TabularInline):
    model = Review
    extra = 0
    fields = ("name", "review")
    # readonly_fields = ("name", "review", "created_at")
    show_change_link = True

# == Exploit INLINE FOR EVENTS ADMIN ==
class ExploitInLine(admin.TabularInline):
    model = Exploit
    extra = 0
    fields = ("name", "vuln", "description")
    show_change_link = True


# == EVENTS ADMIN ==
class EventsAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "author"]
    list_filter = ["created_at"]
    search_fields = ["name", "author"]
    # prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("author",)
    inlines = [VulnsInline, IpAddInline, FQDNInLine, HashInLine, CodeSnippetInLine, ReviewInLine, ExploitInLine]

    # == override save model to set author and lastchange_author ==
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.author = request.user
    #     obj.lastchange_author = request.user
    #     return super().save_model(request, obj, form, change)

# == VULNS ADMIN ==
class VulnsAdmin(admin.ModelAdmin):
    list_display = ["name", "cve", "cvss", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "name"]
    # prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("author",)

    # == override save model to set author and lastchange_author ==
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.author = request.user
    #     obj.lastchange_author = request.user
    #     super().save_model(request, obj, form, change)

# == IPADD ADMIN ==
class IpAdmin(admin.ModelAdmin):
    list_display = ["ip_address", "created_at", "expired_at"]
    list_filter = ["created_at"]
    search_fields = ["ip_address", ]
    readonly_fields = ("author",)

    # == override save model to set author and lastchange_author ==
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.author = request.user
    #     obj.lastchange_author = request.user
    #     super().save_model(request, obj, form, change)

# == CODESNIPPET ADMIN ==
class CodeAdmin(admin.ModelAdmin):
    list_display = ["name", "language", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "language"]
    readonly_fields = ("author",)

    class Meta:
        model = Vuln

    # == override save model to set author and lastchange_author ==
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.author = request.user
    #     obj.lastchange_author = request.user
    #     super().save_model(request, obj, form, change)

# == FQDN ADMIN ==
class FQDNAdmin(admin.ModelAdmin):
    list_display = ["fqdn", "created_at", "expired_at"]
    list_filter = ["created_at"]
    search_fields = ["fqdn"]
    readonly_fields = ("author",)

    # == override save model to set author and lastchange_author ==
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.author = request.user
    #     obj.lastchange_author = request.user
    #     super().save_model(request, obj, form, change)

# == HASH ADMIN ==
class HashAdmin(admin.ModelAdmin):
    list_display = ["filename", "platform", "sha256", "expired_at"]
    list_filter = ["created_at"]
    search_fields = ["sha256", "sha1", "md5"]
    readonly_fields = ("author",)

    # == override save model to set author and lastchange_author ==
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.author = request.user
    #     obj.lastchange_author = request.user
    #     super().save_model(request, obj, form, change)

# == EXPLOIT ADMIN ==
class ExploitAdmin(admin.ModelAdmin):
    list_display = ["name", "event", "vuln", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "event", "vuln"]
    readonly_fields = ("author",)

    # == override save model to set author and lastchange_author ==
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.author = request.user
    #     obj.lastchange_author = request.user
    #     super().save_model(request, obj, form, change)

# == REVIEW ADMIN ==
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "author"]
    list_filter = ["created_at"]
    search_fields = ["name", "author"]
    readonly_fields = ("author",)

    # == override save model to set author and lastchange_author ==
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.author = request.user
    #     obj.lastchange_author = request.user
    #     super().save_model(request, obj, form, change)
    #     return super().save_model(request, obj, form, change)

# == REGISTER MODELS TO ADMIN SITE ==
admin.site.register(Event, EventsAdmin)
admin.site.register(Vuln, VulnsAdmin)
admin.site.register(IpAdd, IpAdmin)
admin.site.register(FQDN, FQDNAdmin)
admin.site.register(Hash, HashAdmin)
admin.site.register(CodeSnippet, CodeAdmin )
admin.site.register(Exploit, ExploitAdmin)
admin.site.register(Review, ReviewAdmin)
