'''This application will store and display the relevant :class:`~papers.models.Publication` objects and associated data.

Current Functionality
=====================

* Includes and displays papers from the lab or other interesting papers.
* Papers are marked up with microdata markup from http://schema.org.  
* There is an API estabished which serves some :class:`~papers.models.Publication` information in json or xml format.  See :mod:`papers.api` for details.
* There will be included comment threads at each paper served by Disqus.
* API's from Altmetric and PLOS are used to also display altmetrics for these papers.
* Papers will also link to author profiles (see the :mod:`personnel` app).
* It is possible to tweet, like (through facebook) or +1 (through google plus) a paper, though the functionality of these are not yet refined.

Longer Term Goals
=================

* Another idea is to have hidden discussions of papers, or papers which are not publicly displayed and require a login.
* Incorporate Mendeley, TotalImpact and PubMedCentral APIs.
* Potentially convert to a facebook app with custom actions and objects.
* Markup with opengraph tags and incorporate twitter cards.
* The :class:`~papers.models.Publication` objects are manually entered but I hope to have these be automatically be generated from CrossRef or Mendeley APIs
'''