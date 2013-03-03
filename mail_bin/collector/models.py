from django.db import models
from django.utils.translation import gettext_lazy as _

VALIDATION_BASIC = 0
VALIDATION_RFC = 1
VALIDATION_MX_RECORD = 2
VALIDATION_SMTP = 3

EMAIL_VALIDATION_LEVELS = [
    (VALIDATION_BASIC, _('Basic')),
    (VALIDATION_RFC, _('Advanced')),
    (VALIDATION_MX_RECORD, _('Mx Record')),
    (VALIDATION_SMTP, _('Smtp')),
]


class WebService(models.Model):

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)
    min_validation_level = models.SmallIntegerField(blank=True, default=0, choices=EMAIL_VALIDATION_LEVELS)

    def __unicode__(self):
        return _("%s (%s)") % (self.name, self.code)


class EmailAddress(models.Model):

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    validation_level = models.SmallIntegerField(default=0, blank=True, choices=EMAIL_VALIDATION_LEVELS)
    verified = models.BooleanField(default=False, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    services = models.ManyToManyField(WebService, through='Subscription')

    def __unicode__(self):
        return self.email


class Subscription(models.Model):

    wants_newsletter = models.BooleanField(default=False, blank=True)
    ip_address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email_address = models.ForeignKey(EmailAddress)
    web_service = models.ForeignKey(WebService)

    def __unicode__(self):
        return _("subscription for %s to %s") % (self.email_address, self.web_service)

