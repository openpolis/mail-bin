from django import forms
from django.utils.translation import gettext as _
from validate_email import validate_email
from mail_bin.collector.models import WebService, VALIDATION_BASIC, VALIDATION_RFC, VALIDATION_MX_RECORD, VALIDATION_SMTP


class SubscribeForm(forms.Form):

    email = forms.EmailField(required=True, min_length=6)
    service = forms.CharField(required=True, min_length=3, max_length=200, widget=forms.HiddenInput)
    validation_level = forms.IntegerField(required=False, initial=0, widget=forms.HiddenInput)
    wants_newsletter = forms.BooleanField(required=False, initial=False)

    def clean(self):

        cleaned_data = super(SubscribeForm, self).clean()

        # check if service is registered
        service_name = cleaned_data.get('service')
        if not service_name:
            return cleaned_data

        try:
            self.service = WebService.objects.get(code=cleaned_data.get('service'))
        except WebService.DoesNotExist:
            self._errors["service"] = self.error_class([_("Servizio non disponibile.")])
            del cleaned_data["service"]
            return cleaned_data

        # email validation (none:0, basic:1, mx_record:2, smtp:3)
        cleaned_data['validation_level'] = level = max(
            cleaned_data.get('validation_level', VALIDATION_BASIC),
            self.service.min_validation_level
        )

        if level == VALIDATION_BASIC:
            return cleaned_data

        email = cleaned_data.get('email')
        if not email:
            return cleaned_data
        validation_params = {}
        if level == VALIDATION_RFC:
            pass
        elif level == VALIDATION_MX_RECORD:
            validation_params['check_mx'] = True
        elif level == VALIDATION_SMTP:
            validation_params['verify'] = True

        # execute email validation
        if not validate_email(email, **validation_params):
            self._errors["email"] = self.error_class([_("L'indirizzo email inserito non esiste.")])
            del cleaned_data["email"]

        return cleaned_data