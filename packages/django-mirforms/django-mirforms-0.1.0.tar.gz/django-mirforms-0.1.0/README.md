=====
mirforms
=====

Mir forms is a Django app contains custom html form inputs.

Quick start
-----------

1. Add "mirforms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mirforms',
    ]

2. Include the mirforms URLconf in your project urls.py like this::

    path('mirforms/', include('mirforms.urls')),