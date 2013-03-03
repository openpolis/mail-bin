from django.contrib import admin
from mail_bin.collector.models import WebService, EmailAddress, Subscription


class WebServiceAdmin(admin.ModelAdmin):
    pass


class SubscriptionInline(admin.StackedInline):
    model = Subscription
    extra = 0


class EmailAdmin(admin.ModelAdmin):
    inlines = [SubscriptionInline, ]


class SubscriptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(WebService, WebServiceAdmin)
admin.site.register(EmailAddress, EmailAdmin)
admin.site.register(Subscription, SubscriptionAdmin)