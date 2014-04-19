"""
This package contains the unit tests for the :mod:`papers` app.

It contains view and model tests for each model, grouped together.
Contains the two model tests:

* :class:`~papers.tests.PublicationModelTests` 
* :class:`~papers.tests.AuthorDetailsModelTests` 

The API tests:

* :class:`~PublicationResourceTests`

And the view tests:

* :class:`~papers.tests.PublicationViewTests` 
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from papers.models import Publication, AuthorDetails, Person, Commentary

MODELS = [Publication, AuthorDetails, Commentary]

class PublicationModelTests(TestCase):
    '''This class tests various aspects of the :class:`~papers.models.Publication` model.'''
    
    fixtures = ['test_publication', 'test_publication_personnel']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def test_create_new_paper_minimum(self):
        '''This test creates a :class:`~papers.models.Publication` with the required information only.'''
        test_publication = Publication(title='Test Publication.')
        test_publication.save()
        self.assertEqual(test_publication.pk, 3)
        
    #def test_create_new_paper_all(self):
        #'''This test creates a `::class:Publication` with the required information only.'''
        #test_publication = Publication(title='Test Publication') #add more fields
        #test_publication.save()        
        
    def test_paper_unicode(self):
        '''This tests the unicode representation of a :class:`~papers.models.Publication`.'''
        test_publication = Publication.objects.get(title_slug='14-3-3-proteins-a-number-of-functions-for-a-numbered-protein')
        self.assertEqual(test_publication.__unicode__(), "14-3-3 proteins: a number of functions for a numbered protein.")
        
    def test_paper_title_slug(self):
        '''This tests the title_slug field of a :class:`~papers.models.Publication`.'''
        test_publication = Publication(title='Test Publication.')
        test_publication.save()
        self.assertEqual(test_publication.title_slug, "test-publication")  
        
    def test_paper_absolute_url(self):
        '''This tests the title_slug field of a :class:`~papers.models.Publication`.'''
        test_publication = Publication(title='Test Publication', laboratory_paper=True)
        test_publication.save()
        self.assertEqual(test_publication.get_absolute_url(), "/papers/test-publication") 
     
    def test_paper_doi_link(self):
        '''This tests the title_slug field of a :class:`~papers.models.Publication`.'''
        test_publication = Publication.objects.get(title="14-3-3 proteins: a number of functions for a numbered protein.")
        self.assertEqual(test_publication.doi_link(), "http://dx.doi.org/10.1126/stke.2962005re10") 
        
    def test_full_pmcid(self):
        '''This tests that a correct full PMCID can be generated for a :class:`~papers.models.Publication`.'''
        test_publication = Publication(title="Test Publication", pmcid = "12345")
        test_publication.save()
        self.assertEqual(test_publication.full_pmcid(), 'PMC12345')                         
                    
class AuthorDetailsModelTests(TestCase):
    '''This class tests varios aspects of the :class:`~papers.models.AuthorDetails` model.'''

    fixtures = ['test_publication', 'test_publication_personnel']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def test_create_new_authordetail_minimum(self):
        '''This test creates a :class:`~papers.models.AuthorDetails` with the required information only.'''
        test_authordetail = AuthorDetails(author=Person.objects.get(pk=1), 
            order = 1)
        test_authordetail.save()
        
    def test_create_new_authordetail_all(self):
        '''This test creates a :class:`~papers.models.AuthorDetails` with the required information only.'''
        test_authordetail = AuthorDetails(author=Person.objects.get(pk=1), 
            order = 1,
            corresponding_author = True,
            equal_contributors = True)
        test_authordetail.save()             
            
    def test_authordetail_unicode(self):
        '''This tests that the unicode representaton of an :class:`~papers.models.AuthorDetails` object is correct.'''
        test_authordetail = AuthorDetails(author=Person.objects.get(pk=1), 
            order = 1)
        test_authordetail.save() 
        self.assertEqual(test_authordetail.__unicode__(), '1 - [] -  Dave Bridges')
        
class CommentaryModelTests(TestCase):
    '''This class tests various aspects of the :class:`~papers.models.Commentary` model.'''
    
    fixtures = ['test_publication', 'test_personnel']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def test_create_new_commentary_minimum(self):
        '''This test creates a :class:`~papers.models.Commentary` with the required information only.'''
        test_commentary = Commentary(paper=Publication.objects.get(pk=1),
            comments = "Some comments")
        test_commentary.save()
        self.assertEqual(test_commentary.pk, 1) 
        
    def test_create_new_commentary_all(self):
        '''This test creates a :class:`~papers.models.Commentary` with all fields entered.'''
        test_commentary = Commentary(paper=Publication.objects.get(pk=1),
            comments = "Some comments",
            author = Person.objects.get(pk=1),
            citation = "some citation")
        test_commentary.save()
        self.assertEqual(test_commentary.pk, 1) 
        
    def test_commentary_unicode(self):
        '''This test creates a :class:`~papers.models.Commentary` and then verifies the unicode representation is correct.'''
        test_commentary = Commentary(paper=Publication.objects.get(pk=1),
            comments = "Some comments")
        test_commentary.save()
        self.assertEqual(test_commentary.__unicode__(), "Journal club summary on 14-3-3 proteins: a number of functions for a numbered protein.")                        
        
class PublicationResourceTests(TestCase):  
    '''This class tests varios aspects of the :class:`~papers.api.PublicationResource` API model.'''

    fixtures = ['test_publication', 'test_publication_personnel']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def api_publication_list_test(self):
        '''This tests that the API correctly renders a list of :class:`~papers.models.Publication` objects.'''
        response = self.client.get('/api/v1/publications/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')
        
    def api_publication_detail_test(self):
        '''This tests that the API correctly renders a particular :class:`~papers.models.Publication` objects.'''
        response = self.client.get('/api/v1/publications/1/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')  
        print response    
       
class PublicationViewTests(TestCase):
    '''This class tests the views for :class:`~papers.models.Publication` objects.'''

    fixtures = ['test_publication', 'test_publication_personnel']

    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_publication_view(self):
        """This tests the paper-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/14-3-3-proteins-a-number-of-functions-for-a-numbered-protein')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication' in test_response.context)        
        self.assertTemplateUsed(test_response, 'paper-detail.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'jquery_script.html') 
        self.assertTemplateUsed(test_response, 'disqus_snippet.html') 
        self.assertTemplateUsed(test_response, 'paper_sharing_widgets.html')
        self.assertTemplateUsed(test_response, 'altmetric_snippet.html')                        
        self.assertEqual(test_response.context['publication'].pk, 1)
        self.assertEqual(test_response.context['publication'].title, u'14-3-3 proteins: a number of functions for a numbered protein.')
        
    def test_lab_papers_list(self):
        """This tests the laboratory-papers view ensuring that templates are loaded correctly.
        
        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication_list' in test_response.context)        
        self.assertTemplateUsed(test_response, 'paper-list.html')
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')   
        self.assertTemplateUsed(test_response, 'paper-detail-snippet.html')
        self.assertEqual(test_response.context['publication_list'][0].pk, 1)
        self.assertEqual(test_response.context['publication_list'][0].title, u'14-3-3 proteins: a number of functions for a numbered protein.')  
        
    def test_interesting_papers_list(self):
        """This tests the interesting-papers view ensuring that templates are loaded correctly.
        
        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/interesting')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication_list' in test_response.context)       
        self.assertTemplateUsed(test_response, 'paper-list.html')
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')   
        self.assertTemplateUsed(test_response, 'paper-detail-snippet.html')                                
        self.assertEqual(test_response.context['publication_list'][0].pk, 2)
        self.assertEqual(test_response.context['publication_list'][0].title, u"THE RELATION OF ADENOSINE-3', 5'-PHOSPHATE AND PHOSPHORYLASE TO THE ACTIONS OF CATECHOLAMINES AND OTHER HORMONES.")           

    def test_publication_view_create(self):
        """This tests the paper-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/new/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'publication_form.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')           

    def test_publication_view_edit(self):
        """This tests the paper-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/14-3-3-proteins-a-number-of-functions-for-a-numbered-protein/edit/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'publication_form.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')        
        self.assertEqual(test_response.context['publication'].pk, 1)
        self.assertEqual(test_response.context['publication'].title, u'14-3-3 proteins: a number of functions for a numbered protein.')

        #verifies that a non-existent object returns a 404 error presuming there is no object with pk=2.
        null_response = self.client.get('/papers/not-a-real-paper/edit/')
        self.assertEqual(null_response.status_code, 404)   

    def test_publication_view_delete(self):
        """This tests the paper-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/14-3-3-proteins-a-number-of-functions-for-a-numbered-protein/delete/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication' in test_response.context)        
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertEqual(test_response.context['publication'].pk, 1)
        self.assertEqual(test_response.context['publication'].title, u'14-3-3 proteins: a number of functions for a numbered protein.')

        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/papers/not-a-real-paper/delete/')
        self.assertEqual(null_response.status_code, 404)  
        
class CommentaryViewTests(TestCase):
    '''This class tests the views for :class:`~papers.models.Commentary` objects.'''

    fixtures = ['test_publication', 'test_personnel', 'test_commentary']

    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_commentary_view(self):
        """This tests the commentary-detail view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/papers/commentary/1')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('commentary' in test_response.context)        
        self.assertTemplateUsed(test_response, 'commentary-detail.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'jquery_script.html') 
        self.assertTemplateUsed(test_response, 'disqus_snippet.html') 
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')                        
        self.assertEqual(test_response.context['commentary'].pk, 1)
        self.assertEqual(test_response.context['commentary'].paper.__unicode__(), u'14-3-3 proteins: a number of functions for a numbered protein.')  
        self.assertEqual(test_response.context['commentary'].comments, "some comments for this fixture")
        
        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/papers/commentary/9999')
        self.assertEqual(null_response.status_code, 404) 
                 
    def test_commentary_view_create(self):
        """This tests the commentary-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/commentary/new')
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'commentary-form.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')                             
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')
        
    def test_commentary_view_edit(self):
        """This tests the commentary-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/commentary/1/edit')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('commentary' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'commentary-form.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')                             
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')
        self.assertEqual(test_response.context['commentary'].pk, 1)
        self.assertEqual(test_response.context['commentary'].paper.__unicode__(), u'14-3-3 proteins: a number of functions for a numbered protein.')  
        self.assertEqual(test_response.context['commentary'].comments, "some comments for this fixture") 
        
        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/papers/commentary/9999/edit')
        self.assertEqual(null_response.status_code, 404) 
        
    def test_commentary_view_delete(self):
        """This tests the commentary-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/commentary/1/delete')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('object' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')   
        
    def test_commentary_view_list(self):
        """This tests the commentary-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/commentaries')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('commentary_list' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'commentary-list.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')                                   
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')  
        self.assertEqual(test_response.context['commentary_list'][0].pk, 1)
        self.assertEqual(test_response.context['commentary_list'][0].paper.__unicode__(), u'14-3-3 proteins: a number of functions for a numbered protein.')  
        self.assertEqual(test_response.context['commentary_list'][0].comments, "some comments for this fixture")                    