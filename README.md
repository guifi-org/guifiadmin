GuifiAdmin
==========

# Quick Setup

Clone the repository

    git clone https://github.com/shagi/guifiadmin.git
    cd guifiadmin

Install depencencies

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

Django setup (https://docs.djangoproject.com/en/1.10/)

    vim guifiadmin/local_settings.py
    python manage.py migrate
    python manage.py runserver

Optionally, install some sample data:

    python manage.py loaddata sample_data/*.json


# Configuration

Override settings editing `guifiadmin/local_settings.py`

To get a list of possible variables:

    cat */*_settings.py
