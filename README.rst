Mail-Bin
========

Mail-Bin provides a url that handle a WebService email subscription::

    http://<site.url>/subscribe[/<service.code>]


Setup
-----

Clone repository::

    git clone git@github.com:openpolis/mail-bin.git

Initialize virtualenv::

    mkvirtualenv mail-bin
    pip install -r requirements.txt


Initialize django::

    cp mail-bin/mail_bin/settings_local.example mail-bin/mail_bin/settings_local.py
    vi mail-bin/mail_bin/settings_local.py
    ... set DATABASES, ALLOWED_HOSTS, SECRET_KEY ...
    python manage.py syncdb
    ...
    python manage.py runserver


Configuration
-------------

Login to Admin and set a current **Site** url and name.
Add your WebService thought the Admin panel, then you can subscribe from external site with *jsonp* request.
Example code is provided by `/subscribe-form/` url, or `/subscribe-form/<service.code>/` and accept a GET params:

-  wants_newsletter = True or False
-  validation_level = 0, 1, 2 or 3


