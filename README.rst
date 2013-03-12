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

    put export MB_SECRET_KEY= ... in virtualenvs - postactivate

    python manage.py syncdb
    python manage.py runserver


Run receiver process::

    python receiver.py

    (use supervisord in production)