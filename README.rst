This project includes the source code for a django/python based biomedical research laboratory website.  This was largely configured for personal use, but is licensed under a CC0 free license, so feel free to copy and modify with no restrictions.


Dependencies and Other Apps
===========================
The two main software dependencies for this project are `Python <http://www.python.org/>`_ and `Django <http://djangoproject.org>`_.  

For detailed installation instructions for Django see `Django Installation Instructions <https://docs.djangoproject.com/en/1.4/topics/install/>`_

The current version uses Python 2.7 and Django 1.4.  

There are two python package dependencies, South and PIL.  If you want to be able to update the documentation you will also need to install Sphinx.  This can be installed with pip by entering on a command line:: 

    pip install South
    pip install PIL
    pip install Sphinx

This project also includes links to three other apps which would have to be installed and configured separately:

* Blog: any blogging software served at http://yourserver/blog
* Protocol Wiki: a wikimedia based protocol site served at http://yourserver/wiki
* MouseDB: a database for animal colony management which can optionally be served at http://yoursever/mousedb.  Based on software available at http://davebridges.github.com/mousedb
* ExperimentDB: a data and laboratory inventory management tool which can optionally be served at http://yourserver/experimentdb.  Uses software available at http://davebridges.github.com/experimentdb

Installation and Setup
======================
1. Clone or download the code and extract it somewhere on your system.
2. Inside the lab_website directory, open **localsettings_empty.py** with a text editor and fill in **'django.db.backends.sqlite3'** under DATABASES... ENGINE and enter a location for your SQLite database to be stored.  To use other database types see the `Django Documentation on Databases <https://docs.djangoproject.com/en/1.4/ref/databases/>`_.
3. Optional:  Fill in the the ADMINS, TIME_ZONE and LANGUAGE_CODE as needed.
4. Run the following command within the Lab Website directory to populate the database.  Enter the superuser information when prompted::

    python manage.py syncdb