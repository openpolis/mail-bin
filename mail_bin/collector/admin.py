from django.contrib import admin
from mail_bin.collector.models import WebService, EmailAddress, Subscription


class WebServiceAdmin(admin.ModelAdmin):
    pass


class SubscriptionInline(admin.StackedInline):
    readonly_fields = ("created_at",)
    model = Subscription
    extra = 0


class EmailAdmin(admin.ModelAdmin):
    inlines = [SubscriptionInline, ]


class SubscriptionAdmin(admin.ModelAdmin):
    list_filter = ('web_service__name', 'created_at')
    search_fields = ('email_address__email', 'first_name', 'last_name')


admin.site.register(WebService, WebServiceAdmin)
admin.site.register(EmailAddress, EmailAdmin)
admin.site.register(Subscription, SubscriptionAdmin)