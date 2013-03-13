#!/usr/bin/env python

import os
import zmq
import json
import logging
from validate_email import validate_email

logger = logging.getLogger('mail_bin')


def store_req_handler(url, models):

    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.bind(url)

    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)

    logger.info(u"Listening to save requests from the world on {0}".format(url))

    while True:
        socks = dict(poller.poll())

        if receiver in socks and socks[receiver] == zmq.POLLIN:
            message = json.loads(receiver.recv())

            logger.debug(u"Save request: {0}".format(message))

            service_uri = message.pop('service_uri', None)
            if not service_uri:
                logger.debug(u"WebService URI not found")
                continue

            try:
                service = models.WebService.objects.get(uri=service_uri)

                email_address = message.pop('email', None)
                if not (email_address and validate_email(email_address)):
                    logger.debug(u'Invalid mail address "{0}"'.format(email_address))
                    continue

                service.subscribe(email_address, **message)

            except models.WebService.DoesNotExist:
                logger.debug(u"WebService URI not exists: {0}".format(service_uri))


if __name__ == "__main__":

    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mail_bin.settings")
    from django.conf import settings
    from mail_bin.collector import models

    try:
        store_req_handler(settings.QUEUE_URL, models)
    except KeyboardInterrupt:
        logger.info("Closing service...")
        pass

