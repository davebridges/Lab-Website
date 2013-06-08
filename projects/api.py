'''This package controls API access to the :mod:`projects` app.

Overview
--------

The API for the :mod:`projects` application provides data on research projectss.  The data can be provided as either a group of projects or as a single project.  Only GET requests are accepted.
These urls are served at the endpoint **/api/v1/projects/**, and depends on your server url.  For these examples we will presume that you can reach this endpoint at **http://yourserver.org/api/v1/publications/**.  Currently for all requests, no authentication is required.  The entire API schema is available at::

    http://yourserver.org/api/v1/projects/schema/?format=xml
    http://yourserver.org/api/v1/projects/schema/?format=json
    

Sample Code
-----------

Either group requests or single project requests can be served depending on if the primary key is provided.  The request URI has several parts including the servername, the api version (currently v1) then the item type (projects).  There must be a trailing slash before the request parameters (which are after a **?** sign and separated by a **&** sign).  All of these sample codes show a json returned, but ?format=json can be replaced with ?format=xml to retrieve these data in XML format.

For a collection of projects
````````````````````````````

For a collection of projects you can request::

    http://yourserver.org/api/v1/projects/?format=json 
    
This would return all projects in the database.  
The meta object contains fields for the limit, next, offset, previous and total_count for the series of objects requested.  The objects portion is an array of the returned publications.  Note the id field of a publication.  This is used for retrieving a single publication.  Collections can also be filtered based on type or year::

    http://yourserver.org/api/v1/project/?format=json
    http://yourserver.org/api/v1/projects/set/1;3/?format=json 
    
The last example requests the projects with id numbers 1 and 3.                    

For a single project
````````````````````

To retrieve a single projects you need to know the primary key of the object.  This can be found from the id parameter of a collection (see above) or from the actual object page.  You can retrieve details about a single article with a call such as::

    http://yourserver.org/api/v1/projects/2/?format=json  
    
In this case **2** is the primary key (or id field) of the projects in question.


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
| start_date       | **2012-12-24**                          |
+------------------+-----------------------------------------+
| limit            | **0** for all, any other number         |
+------------------+-----------------------------------------+

Response Values
```````````````

The response (in either json or xml) provides the following fields for each object (or for the only object in the case of a single object request).

+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
|      Field         |              Explanation                            |                         Sample Value                        |
+====================+=====================================================+=============================================================+
| absolute_url       | the url of the page on this site                    | /project/some-project                                       |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 
| date_added         | data added to this database                         | 2012-08-18                                                  |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| date_last_modified | last modified in database                           | 2012-08-25                                                  |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| id                 | the primary key of the object                       | 1                                                           |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| priority           | the priority of the project (1 is low, 5 is high)   | 1                                                           |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| resource_uri       | a link to the api for this publication              | /api/v1/publications/1/                                     |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| start_date         | the start date of the project                       | 2012-08-25                                                  | 
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| summary            | the summary of the project                          | a written summary of the project                            | 
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| title              | the title of the paper                              | TC10 Is Regulated by Caveolin in 3T3-L1 Adipocytes.         |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
| title_slug         | slugified title of the paper                        | tc10-is-regulated-by-caveolin-in-3t3-l1-adipocytes          |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+

'''

from tastypie.resources import ModelResource

from projects.models import Project

class ProjectResource(ModelResource):
    '''This generates the API resource for :class:`~projects.models.Project` objects.
    
    It returns all projects in the database.
    There are no direct links from this to either Personnel or Publication objects.
    '''
    
    class Meta:
        '''The API serves all :class:`~projects.models.Project` objects in the database..'''
        queryset = Project.objects.all()
        resource_name = 'projects'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get'] 
        include_absolute_url = True
        filtering = {
            "start_date": ('exact', 'contains')
        }      
               