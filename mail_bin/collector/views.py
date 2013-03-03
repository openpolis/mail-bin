import json
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.translation import gettext as _
from mail_bin.collector.forms import SubscribeForm
from mail_bin.collector.models import EmailAddress, Subscription, WebService


def json_response(func):
    """
    source: https://coderwall.com/p/k8vb_a
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except TypeError:
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator


@json_response
def confirm(request):
    pass


def subscribe_form(request, service=None):
    from django.shortcuts import render
    from django.contrib.sites.models import Site
    from django.core.urlresolvers import reverse

    form = SubscribeForm()

    min_validation_level = 0
    if service:
        try:
            web_service = WebService.objects.get(code=service)
            form.initial['service'] = web_service.code
            min_validation_level = web_service.min_validation_level
        except WebService.DoesNotExist:
            return HttpResponseBadRequest("Invalid service '{0}'".format(service))
    else:
        form.fields['service'].widget = forms.Select(choices=[(ws.code, ws.name) for ws in WebService.objects.all()])

    if not request.GET.get('wants_newsletter') is None:
        form.initial['wants_newsletter'] = request.GET.get('wants_newsletter').lower() in ('1', 'on', 'ok', 'true')
        form.fields['wants_newsletter'].widget = forms.HiddenInput()

    try:
        validation_level = int(request.GET.get('validation_level', min_validation_level))
    except ValueError:
        validation_level = min_validation_level
    form.initial['validation_level'] = validation_level

    return render(request, 'subscription_form.html', {
        'form': form,
        'url': 'http://%s%s' % (Site.objects.get_current().domain, reverse('subscribe'))
    })


@json_response
def subscribe(request, service=None):

    data = request.GET.copy()
    if service:
        data['service'] = service

    # A form bound to the GET data
    form = SubscribeForm(data)

    if form.is_valid():

        # create email address
        email_address, email_created = EmailAddress.objects.get_or_create(
            email=form.cleaned_data.get('email'),
            defaults=dict(
                validation_level=form.cleaned_data.get('validation_level'),
            )
        )
        if not email_created and email_address.validation_level != form.cleaned_data.get('validation_level'):
            # update email validation level
            email_address.validation_level = form.cleaned_data.get('validation_level')
            email_address.save()

        # create subscription
        subscription, subscription_created = Subscription.objects.get_or_create(
            email_address=email_address,
            web_service=form.service,
            defaults=dict(
                ip_address=request.META.get('REMOTE_ADDR'),
                wants_newsletter=form.cleaned_data.get('wants_newsletter'),
            )
        )
        if not subscription_created and subscription.wants_newsletter != form.cleaned_data.get('wants_newsletter'):
            # update subscription params
            subscription.wants_newsletter = form.cleaned_data.get('wants_newsletter')
            subscription.ip_address = request.META.get('REMOTE_ADDR')
            subscription.save()

        return {
            'result': request.GET.get('success_message', _('Registrazione avvenuta correttamente'))
        }
    return {
        'errors_txt': "{0}".format(form.errors),
        'errors': dict(form.errors.items())
    }