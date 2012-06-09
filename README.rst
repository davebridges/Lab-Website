This project includes the source code for a django/python based biomedical research laboratory website.  This was largely configured for personal use, but is licensed under a CC0 free license, so feel free to copy and modify with no restrictions.


Dependencies and Other Apps
===========================
The two main software dependencies for this project are `Python <http://www.python.org/>`_ and `Django <http://djangoproject.org>`_.  

For detailed installation instructions for Django see `Django Installation Instructions <https://docs.djangoproject.com/en/1.4/topics/install/>`_

The current version uses Python 2.7 and Django 1.4

This project also includes links to three other apps which would have to be installed and configured separately:

* Blog: any blogging software served at http://yourserver/blog
* Protocol Wiki: a wikimedia based protocol site served at http://yourserver/wiki
* MouseDB: a database for animal colony management which can optionally be served at http://yoursever/mousedb.  Based on software available at http://davebridges.github.com/mousedb
* ExperimentDB: a data and laboratory inventory management tool which can optionally be served at http://yourserver/experimentdb.  Uses software available at http://davebridges.github.com/experimentdb