'''This application will store and display the relevant :class:`~projects.models.Project` objects and associated data.

Current Functionality
=====================

* Displays and summarizes current and previous lab projects.
* There is a comment threads at each project served by Disqus.
* Projects are marked up with microdata markup from http://schema.org.  
* There is an API estabished which serves some :class:`~papers.models.Publication` information in json or xml format.  See :mod:`papers.api` for details.
* There is a comment threads at each project served by Disqus.
* Projects will also link to the people working on that project (see the :mod:`personnel` app).
* Projects will also link to publications (see the :mod:`papers` app).
* It is possible to tweet, like (through facebook) or +1 (through google plus) a project, though the functionality of these are not yet refined.

Longer Term Goals
=================

* Another idea is to have hidden discussions of projects, or projects which are not publicly displayed and require a login.
* Projects will also link to publications (see the :mod:`papers` app).
* It is possible to tweet, like (through facebook) or +1 (through google plus) a project, though the functionality of these are not yet refined.
* Potentially convert to a facebook app with custom actions and objects.
* Markup with opengraph tags and incorporate twitter cards.
'''