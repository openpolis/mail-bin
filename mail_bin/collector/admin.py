from django.contrib import admin
from mail_bin.collector.models import WebService, EmailAddress, Subscription


class CSVAdmin(admin.ModelAdmin):
    """
    Adds a CSV export action to an admin view.
    """

    # This is the maximum number of records that will be written.
    # Exporting massive numbers of records should be done asynchronously.
    csv_record_limit = 1000

    extra_csv_fields = ()

    def get_actions(self, request):
        actions = self.actions if hasattr(self, 'actions') else []
        actions.append('csv_export')
        actions = super(CSVAdmin, self).get_actions(request)
        return actions

    def get_extra_csv_fields(self, request):
        return self.extra_csv_fields

    def csv_export(self, request, qs=None, *args, **kwargs):
        import csv
        from django.http import HttpResponse
        from django.template.defaultfilters import slugify

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' \
                                          % slugify(self.model.__name__)
        headers = list(self.list_display) + list(self.get_extra_csv_fields(request))

        try:
            headers.remove('__str__')
        except ValueError, AttributeError:
            pass
        try:
            headers.remove('__unicode__')
        except ValueError, AttributeError:
            pass

        if len(headers) is 0:
            return HttpResponse(status=500, content='no csv data, specify an extra_csv_fields parameter in your admin class')

        writer = csv.DictWriter(response, headers)

        # Write header.
        header_data = {}
        for name in headers:
            if hasattr(self, name) \
                and hasattr(getattr(self, name), 'short_description'):
                header_data[name] = getattr(
                    getattr(self, name), 'short_description')
            else:
                field = self.model._meta.get_field_by_name(name)
                if field and field[0].verbose_name:
                    header_data[name] = field[0].verbose_name
                else:
                    header_data[name] = name
            header_data[name] = header_data[name].title()
        writer.writerow(header_data)

        # Write records.
        for r in qs[:self.csv_record_limit]:
            data = {}
            for name in headers:
                if hasattr(r, name):
                    data[name] = getattr(r, name)
                elif hasattr(self, name):
                    data[name] = getattr(self, name)(r)
                else:
                    raise Exception, 'Unknown field: %s' % (name,)

                if callable(data[name]):
                    data[name] = data[name]()
            writer.writerow(data)
        return response
    csv_export.short_description = \
        'Exported selected %(verbose_name_plural)s as CSV'


class WebServiceAdmin(admin.ModelAdmin):
    pass


class SubscriptionInline(admin.StackedInline):
    readonly_fields = ("created_at",)
    model = Subscription
    extra = 0


class EmailAdmin(admin.ModelAdmin):
    inlines = [SubscriptionInline, ]


class SubscriptionAdmin(CSVAdmin):
    extra_csv_fields = ('first_name', 'last_name', 'email_address')
    list_filter = ('web_service__name', 'created_at')
    search_fields = ('email_address__email', 'first_name', 'last_name')


admin.site.register(WebService, WebServiceAdmin)
admin.site.register(EmailAddress, EmailAdmin)
admin.site.register(Subscription, SubscriptionAdmin)