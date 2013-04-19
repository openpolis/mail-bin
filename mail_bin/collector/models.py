from django.db import models
import logging
logger = logging.getLogger('mail_bin')

VALIDATION_BASIC = 0
VALIDATION_RFC = 1
VALIDATION_MX_RECORD = 2
VALIDATION_SMTP = 3

EMAIL_VALIDATION_LEVELS = [
    (VALIDATION_BASIC, 'Basic'),
    (VALIDATION_RFC, 'Advanced'),
    (VALIDATION_MX_RECORD, 'Mx Record'),
    (VALIDATION_SMTP, 'Smtp'),
]


def update_name(obj, first_name, last_name):
    edited = False
    if not obj.first_name and first_name:
        obj.first_name = first_name
        edited = True
    if not obj.last_name and last_name:
        obj.last_name = last_name
        edited = True
    if edited:
        obj.save()
    return edited


class EmailAddress(models.Model):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #validation_level = models.SmallIntegerField(default=0, blank=True, choices=EMAIL_VALIDATION_LEVELS)

    services = models.ManyToManyField('WebService', through='Subscription')

    class Meta:
        verbose_name = 'Indirizzo email'
        verbose_name_plural = 'Indirizzi email'

    def __unicode__(self):
        return self.email


class Subscription(models.Model):

    ip_address = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    email_address = models.ForeignKey('EmailAddress')
    web_service = models.ForeignKey('WebService')

    class Meta:
        verbose_name = 'Iscrizione'
        verbose_name_plural = 'Iscrizioni'

    def __unicode__(self):
        return u"{0} a {1} - {2}".format(self.email_address, self.web_service, self.created_at)


class WebService(models.Model):

    name = models.CharField(max_length=200)
    uri = models.URLField(unique=True)
    #min_validation_level = models.SmallIntegerField(blank=True, default=0, choices=EMAIL_VALIDATION_LEVELS)

    def subscribe(self, email, ip_address='', user_agent='', last_name='', first_name=''):

        # create email address
        email_address, email_created = EmailAddress.objects.get_or_create(
            email=email,
            defaults=dict(
                first_name=last_name,
                last_name=first_name,
            )
        )
        if email_created:
            logger.debug(u"New email: {0}".format(email_address))
        else:
            if update_name(email_address, first_name, last_name):
                logger.debug(u"Email updated: {0}".format(email_address))
            else:
                logger.debug(u"Email already registered: {0}".format(email_address))

        # create subscription
        subscription, subscription_created = Subscription.objects.get_or_create(
            email_address=email_address,
            web_service=self,
            defaults=dict(
                ip_address=ip_address,
                user_agent=user_agent,
                first_name=last_name,
                last_name=first_name,
            )
        )
        if subscription_created:
            logger.debug(u"New subscription: {0}".format(subscription))
        else:
            if update_name(subscription, first_name, last_name):
                logger.debug(u"Subscription updated: {0}".format(subscription))
            else:
                logger.debug(u"Subscription already created: {0}".format(subscription))

        return subscription_created

    class Meta:
        verbose_name = 'Servizio'
        verbose_name_plural = 'Servizi'

    def __unicode__(self):
        return self.name