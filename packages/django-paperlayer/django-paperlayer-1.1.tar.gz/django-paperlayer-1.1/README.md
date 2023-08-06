Paperlayer
=====

Paperlayer is a platform that enables academics to come together in their new projects using Dajngo app.

Detailed documentation is in the github directory. (https://github.com/bounswe/bounswe2020group3/wiki)

Quick start
-----------

1. Add "paperlayer" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'paperlayer',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('', include('paperlayer.backend.urls')),

3. Run ``python manage.py migrate`` to create the paperlayer models.

4. Run ``python manage.py createsuperuser``to create new admin user.

5. Start the development server and visit http://127.0.0.1:8000/swagger/
   to see all APIs.