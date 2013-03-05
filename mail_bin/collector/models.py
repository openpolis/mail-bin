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


class EmailAddress(models.Model):

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #validation_level = models.SmallIntegerField(default=0, blank=True, choices=EMAIL_VALIDATION_LEVELS)

    services = models.ManyToManyField('WebService', through='Subscription')

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

    def __unicode__(self):
        return u"subscription for {0} to {1}".format(self.email_address, self.web_service)


class WebService(models.Model):

    name = models.CharField(max_length=200)
    uri = models.URLField(unique=True)
    #min_validation_level = models.SmallIntegerField(blank=True, default=0, choices=EMAIL_VALIDATION_LEVELS)

    def subscribe(self, email, ip='', user_agent='', last_name='', first_name='', created_at=None):

        # create email address
        email_address, email_created = EmailAddress.objects.get_or_create(
            email=email,
        )
        if email_created:
            logger.debug(u"New email: {0}".format(email_address))
        else:
            logger.debug(u"Email already registered: {0}".format(email_address))

        # create subscription
        subscription, subscription_created = Subscription.objects.get_or_create(
            email_address=email_address,
            web_service=self,
            defaults=dict(
                ip_address=ip,
                user_agent=user_agent,
                first_name=last_name,
                last_name=first_name,
                created_at=created_at
            )
        )
        if subscription_created:
            logger.debug(u"New subscription: {0}".format(subscription))
        else:
            logger.debug(u"Subscription already created: {0}".format(subscription))

        return subscription_created

    def __unicode__(self):
        return self.name