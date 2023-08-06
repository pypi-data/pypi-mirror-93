=====
Ferdowsi_Cal
=====

Ferdowsi_Cal is a simple Django app that provides 4 calendars:
1. gregorian admin calendar
2. gregorian user calendar
3. persian admin calendar
4. persian user calendar

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "Ferdowsi_Cal" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
        'Ferdowsi_Cal',
    ]
	
2. Add "Ferdowsi_Cal" to your TEMPLATES's DIR like this:

	TEMPLATES = [
		{
			...
			'DIRS': [
					...
					os.path.join(BASE_DIR, 'Ferdowsi_Cal', 'templates')],
					...
			...
		},
	]

3. Include the Ferdowsi_Cal URLconf in your project urls.py like this:

    path('', include('Ferdowsi_Cal.urls')),

4. Run `python manage.py migrate` to create the Ferdowsi_Cal models.

5. Use {% load my_tags %} inside your template files and then use tage.
6. There are 5 tags that you can use:
	{% Gregorian_calendar admin=True %}
	{% Gregorian_calendar admin=False %}
	{% Persian_calendar admin=True %}
	{% Persian_calendar admin=False %}
	{% Diagram app='YourAppName' model='YourModelName' column='ColumnName' fkey='ForeignKeyName' %}