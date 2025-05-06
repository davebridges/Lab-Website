'''This package controls API access to the :mod:`personnel` app.

Overview
--------

The API for the :mod:`personnel` application provides data on people.  The data can be provided as either a group of people or as a single person.  Only GET requests are accepted.
These urls are served at the endpoint **/api/v1/personnel/**, and depends on your server url.  For these examples we will presume that you can reach this endpoint at **http://yourserver.org/api/v1/personnel/**.  Currently for all requests, no authentication is required.  The entire API schema is available at::

    http://yourserver.org/api/v1/personnel/schema/?format=xml
    http://yourserver.org/api/v1/personnel/schema/?format=json
    

Sample Code
-----------

Either group requests or single person requests can be served depending on if the primary key is provided.  The request URI has several parts including the servername, the api version (currently v1) then the item type (personnel).  There must be a trailing slash before the request parameters (which are after a **?** sign and separated by a **&** sign).

For a collection of personnel
````````````````````````````````

For a collection of personnel you can request::

    http://yourserver.org/api/v1/personnel/?format=json 
    
This would return all current lab personnel in the database.  This would return the following json response with two JSON objects, meta and objects.
The meta object contains fields for the limit, next, offset, previous and total_count for the series of objects requested.  The objects portion is an array of the returned personnel.  Note the id field of a publication.  This is used for retrieving a single person::

    http://yourserver.org/api/v1/personnel/?format=json     
    http://yourserver.org/api/v1/publications/set/1;3/?format=json 
    
The last example requests the personnel with id numbers 1 and 3.                    

For a single person
````````````````````

To retrieve a single person you need to know the primary key of the object.  This can be found from the id parameter of a collection (see above) or from the actual object page.  You can retrieve details about a single article with a call such as::

    http://yourserver.org/api/v1/personnel/2/?format=json  
    
In this case **2** is the primary key (or id field) of the person in question.


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
| limit            | **0** for all, any other number         |
+------------------+-----------------------------------------+

Response Values
```````````````

The response (in either json or xml) provides the following fields for each object (or for the only object in the case of a single object request).

+--------------------+-----------------------------------------------------+---------------------------------+
|      Field         |              Explanation                            |          Sample Value           |
+====================+=====================================================+=================================+
| absolute_url       | the url of the page on this site                    | /people/dave-bridges/           |
+--------------------+-----------------------------------------------------+---------------------------------+ 
| additional_names   | middle or other names                               | Edward                          |
+--------------------+-----------------------------------------------------+---------------------------------+
| biography          | personal biography                                  | some text                       |
+--------------------+-----------------------------------------------------+---------------------------------+
| birthdate          | date of birth                                       | 1978-12-24                      |
+--------------------+-----------------------------------------------------+---------------------------------+
| current_lab_member | whether this is a current lab member                | true                            |
+--------------------+-----------------------------------------------------+---------------------------------+
| created            | date this entry was created                         | 2012-08-25                      |
+--------------------+-----------------------------------------------------+---------------------------------+
| current_lab_member | whether this is a current lab member                | true                            |
+--------------------+-----------------------------------------------------+---------------------------------+
| first_name         | given name                                          | Dave                            |
+--------------------+-----------------------------------------------------+---------------------------------+
| gender             |                                                     | male                            |
+--------------------+-----------------------------------------------------+---------------------------------+
| id                 | the primary key for the person                      | 1                               |
+--------------------+-----------------------------------------------------+---------------------------------+
| image              | an image of the person                              |                                 |
+--------------------+-----------------------------------------------------+---------------------------------+
| last_name          | family name                                         | Bridges                         |
+--------------------+-----------------------------------------------------+---------------------------------+ 
| name_slug          | slugified name                                      | dave-bridges                    |
+--------------------+-----------------------------------------------------+---------------------------------+
| phone              | phone number                                        |                                 |
+--------------------+-----------------------------------------------------+---------------------------------+
| resource_uri       | a link to the api for this publication              | /api/v1/personnel/1/            |
+--------------------+-----------------------------------------------------+---------------------------------+
| twitter_username   | username if on twitter                              | bridges_lab                     |
+--------------------+-----------------------------------------------------+---------------------------------+
| updated            | when was this entry updated                         | 2013-04-20                      |
+--------------------+-----------------------------------------------------+---------------------------------+
| website            | personal website                                    | http://davebridges.github.com   |
+--------------------+-----------------------------------------------------+---------------------------------+   

'''

from tastypie.resources import ModelResource

from personnel.models import Person

class PersonnelResource(ModelResource):
    '''This generates the API resource for :class:`~personnel.models.Person` objects.
    
    It returns all current lab personnel in the database.
    Currently this does not integrate any information about their role in the lab.
    '''
    
    class Meta:
        '''The API serves only :class:`~personnel.models.Person` objects in the database, who are identified as current lab members.'''
        queryset = Person.objects.filter(current_lab_member=True)
        resource_name = 'personnel'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get'] 
        include_absolute_url = True   
        excludes = ['email', 'facebook_user_id', 'google_plus_user_id', 'phone']
               
