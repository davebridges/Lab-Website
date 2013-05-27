This project includes the source code for a django/python based biomedical research laboratory website.  This was largely configured for personal use, but is licensed under a CC0 free license, so feel free to copy and modify with no restrictions.


Installation and Setup
======================
1. Clone or download this code and extract it somewhere on your system.
2. Inside the lab_website directory, open **localsettings_empty.py** with a text editor and fill in **'django.db.backends.sqlite3'** under DATABASES... ENGINE and enter a location for your SQLite database to be stored under NAME.  To use other database types see the `Django Documentation on Databases <https://docs.djangoproject.com/en/1.4/ref/databases/>`_.
3. Optional:  Fill in the the ADMINS, TIME_ZONE and LANGUAGE_CODE as needed.  
4. Save this file as **localsettings.py** in the same directory.
4. Run the following command within the Lab Website directory to populate the database.  Enter the superuser information when prompted::

    python manage.py schemamigration communication --initial
    python manage.py schemamigration papers --initial
    python manage.py schemamigration personnel --initial
    python manage.py migrate
    python manage.py syncdb
    
Testing
--------
Run the test suite with::

    python manage.py test
    
In localsettings.py, set Debug=FALSE when you have verified everything is working.    
    
Dependencies and Other Apps
===========================
The two main software dependencies for this project are `Python <http://www.python.org/>`_ and `Django <http://djangoproject.org>`_.  You will require a database backend and a webserver for proper function.  For detailed installation instructions for Django see `Django Installation Instructions <https://docs.djangoproject.com/en/1.4/topics/install/>`_

The current version uses Python 2.7 and Django 1.4.  

To install python dependencies, entering on a command line:: 

    pip install -r requirements.txt
    
Another python package dependency is the python-oauth2 library.  This can be downloaded and installed from https://github.com/brosner/python-oauth2.

This project also includes links to three other apps which would have to be installed and configured separately:

* Blog: any blogging software served at http://yourserver/blog
* Protocol Wiki: a wikimedia based protocol site served at http://yourserver/wiki
* MouseDB: a database for animal colony management which can optionally be served at http://yoursever/mousedb.  Based on software available at http://github.com/davebridges/mousedb
* ExperimentDB: a data and laboratory inventory management tool which can optionally be served at http://yourserver/experimentdb.  Uses software available at https://github.com/davebridges/ExperimentDB    
    