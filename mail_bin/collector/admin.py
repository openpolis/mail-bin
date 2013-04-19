from django.contrib import admin
from django.http import HttpResponse
from mail_bin.collector.models import WebService, EmailAddress, Subscription
import csv


def export_select_fields_csv_action(description="Export selected objects as CSV file",
                                    fields=None, exclude=None, header=True):
    """
    This function returns an export csv action

    'fields' is a list of tuples denoting the field and label to be exported. Labels
    make up the header row of the exported file if header=True.

        fields=[
                ('field1', 'label1'),
                ('field2', 'label2'),
                ('field3', 'label3'),
            ]

    'exclude' is a flat list of fields to exclude. If 'exclude' is passed,
    'fields' will not be used. Either use 'fields' or 'exclude.'

        exclude=['field1', 'field2', field3]

    'header' is whether or not to output the column names as the first row

    Based on: http://djangosnippets.org/snippets/2020/
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]
        labels = []
        if exclude:
            field_names = [v for v in field_names if v not in exclude]
        elif fields:
            field_names = [k for k, v in fields if k in field_names]
            labels = [v for k, v in fields if k in field_names]

        response = HttpResponse(mimetype='text/plain; charset=utf8')



        # uncomment this if download is required
        #response = HttpResponse(mimetype='text/csv')
        #response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            if labels:
                writer.writerow(labels)
            else:
                writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode('utf-8') for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv


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
    actions = [
        export_select_fields_csv_action("Esporta i selezionati in formato CSV",
             fields=[
                 ('first_name', 'Nome'),
                 ('last_name', 'Cognome'),
                 ('email_address', 'Email'),
             ],
             header=True
        ),
    ]


admin.site.register(WebService, WebServiceAdmin)
admin.site.register(EmailAddress, EmailAdmin)
admin.site.register(Subscription, SubscriptionAdmin)