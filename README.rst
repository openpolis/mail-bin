Mail-Bin
========

Setup
-----

Clone repository::

    git clone git@github.com:openpolis/mail-bin.git

Initialize virtualenv::

    cd mail_bin
    mkvirtualenv mail-bin
    setvirtualenvproject
    pip install -r requirements.txt


Initialize django::

    cp mail-bin/mail_bin/settings_local.example mail-bin/mail_bin/settings_local.py
    vi mail-bin/mail_bin/settings_local.py
    ... set DATABASES, SECRET_KEY, LOGGING ...
    python manage.py syncdb
    ...
    python manage.py runserver

