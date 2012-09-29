'''This package controls API access to the :mod:`papers` app.

Overview
--------

The API for the :mod:`papers` application provides data on publications.  The data can be provided as either a group of publications or as a single publication.  Only GET requests are accepted.
These urls are served at the endpoint **/api/v1/publications/**, and depends on your server url.  For these examples we will presume that you can reach this endpoint at **http://yourserver.org/api/v1/publications/**.  Currently for all requests, no authentication is required.  The entire API schema is available at::

    http://yourserver.org/api/v1/publications/schema/?format=xml
    http://yourserver.org/api/v1/publications/schema/?format=json
    

Sample Code
-----------

Either group requests or single publication requests can be served depending on if the primary key is provided.  The request URI has several parts including the servername, the api version (currently v1) then the item type (publications).  There must be a trailing slash before the request parameters (which are after a **?** sign and separated by a **&** sign).

For a collection of publications
````````````````````````````````

For a collection of publications you can request::

    http://yourserver.org/api/v1/publications/?format=json 
    
This would return all publications in the database.  This would return the following json response with two JSON objects, meta and objects.
The meta object contains fields for the limit, next, offset, previous and total_count for the series of objects requested.  The objects portion is an array of the returned publications.  Note the id field of a publication.  This is used for retrieving a single publication.  Collections can also be filtered based on type or year::

    http://yourserver.org/api/v1/publications/?format=json&year=2012     
    http://yourserver.org/api/v1/publications/?format=json&type=journal-article 
    http://yourserver.org/api/v1/publications/?format=json&type=journal-article&year=2012
    http://yourserver.org/api/v1/publications/set/1;3/?format=json 
    
The last example requests the publications with id numbers 1 and 3.                    

For a single publication
````````````````````````

To retrieve a single publication you need to know the primary key of the object.  This can be found from the id parameter of a collection (see above) or from the actual object page.  You can retrieve details about a single article with a call such as::

    http://yourserver.org/api/v1/publications/2/?format=json  
    
In this case **2** is the primary key (or id field) of the publication in question.


Reference
---------

Request Parameters
``````````````````

The following are the potential request variables.  You must supply a format, but can also filter based on other parameters.  By default 20 items are returned but you can increase this to all by setting limit=0.

+------------------+-----------------------------------------+
| Parameter        | Potential Values                        |
+==================+=========================================+
| format           | **json** or **xml**                     |
+------------------+-----------------------------------------+
| year             | **2008**                                |
+------------------+-----------------------------------------+
| type             | **journal-article** or **book-section** |
+------------------+-----------------------------------------+
| laboratory_paper | **true** or **false**                   |
+------------------+-----------------------------------------+
| limit            | **0** for all, any other number         |
+------------------+-----------------------------------------+

Response Values
```````````````

The response (in either json or xml) provides the following fields for each object (or for the only object in the case of a single object request).

+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
|      Field         |              Explanation                            |                         Sample Value                        |
+====================+=====================================================+=============================================================+
| absolute_url       | the url of the page on this site                    | /papers/tc10-is-regulated-by-caveolin-in-3t3-l1-adipocytes/ |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 
| abstract           | abstract or summary                                 | some text...                                                |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| date_added         | data added to this database                         | 2012-08-18                                                  |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| date_last_modified | last modified in database                           | 2012-08-25                                                  |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| doi                | digital object identifier                           | 10.1371/journal.pone.0042451                                |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| id                 | the database id number                              | 1                                                           |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 
| interesting_paper  | whether the paper is marked as an interesting paper | false                                                       |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| issue              | the issue of the journal                            | 8                                                           |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| journal            | the name of the journal                             | PLOS One                                                    |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| laboratory_paper   | whether the paper is from this laboratory           | true                                                        |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| mendeley_id        | the mendeley id number for the paper                | null                                                        |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| mendeley_url       | the mendeley url for the paper                      |                                                             |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| pages              | page range for the paper                            | e42451                                                      |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 
| pmcid              | PubMed Central id number                            | null                                                        |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| pmid               | PubMed id number                                    | 22900022                                                    |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| resource_uri       | a link to the api for this publication              | /api/v1/publications/1/                                     |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| title              | the title of the paper                              | TC10 Is Regulated by Caveolin in 3T3-L1 Adipocytes.         |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| title_slug         | slugified title of the paper                        | tc10-is-regulated-by-caveolin-in-3t3-l1-adipocytes          |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| type               | type of publication                                 | journal-article                                             |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+   
| volume             | volume of the article in a journal                  | 7                                                           |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| year               | publication year                                    | 2012                                                        |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+

'''

from tastypie.resources import ModelResource

from papers.models import Publication

class PublicationResource(ModelResource):
    '''This generates the API resource for :class:`~papers.models.Publication` objects.
    
    It returns all publications in the database.
    Authors are currently not linked, as that would require an API to the :mod:`personnel` app.
    '''
    
    class Meta:
        '''The API serves all :class:`~papers.models.Publication` objects in the database..'''
        queryset = Publication.objects.all()
        resource_name = 'publications'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get'] 
        include_absolute_url = True
        filtering = {
            "year": 'exact',
            "type": ('exact', 'contains',),
            "laboratory_paper": 'exact',
        }      
               