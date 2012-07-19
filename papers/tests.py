"""
This package contains the unit tests for the papers app.

It contains view and model tests for each model, grouped together.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from papers.models import Publication, AuthorDetails


class PublicationModelTests(TestCase):
    '''This class tests varios aspects of the `::class:Publication` model.'''
    fixtures = ['fixture_publication']

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
        '''This test creates a `::class:Publication` with the required information only.'''
        test_publication = Publication(title='Test Publication')
        test_pubilcation.save()
        
    def test_create_new_paper_all(self):
        '''This test creates a `::class:Publication` with the required information only.'''
        test_publication = Publication(title='Test Publication') #add more fields
        test_pubilcation.save()        
        
    def test_paper_unicode(self):
        '''This tests the unicode representation of a `::class:Publication`.'''
        test_publication = Publication(title='Test Publication')
        test_pubilcation.save()
        self.AssertEqual(test_publication.__unicode__(), "Test Publication")
        
    def test_paper_title_slug(self):
        '''This tests the title_slug field of a `::class:Publication`.'''
        test_publication = Publication(title='Test Publication')
        test_pubilcation.save()
        self.AssertEqual(test_publication.title_slug, "test-publication")  
        
    def test_paper_absolute_url(self):
        '''This tests the title_slug field of a `::class:Publication`.'''
        test_publication = Publication(title='Test Publication')
        test_pubilcation.save()
        self.AssertEqual(test_publication.get_absolute_url, "/papers/test-publication") 
     
    def test_paper_doi_link(self):
        '''This tests the title_slug field of a `::class:Publication`.'''
        test_publication = Publication(title='Test Publication', doi='10.1126/stke.2422004re10')
        test_pubilcation.save()
        self.AssertEqual(test_publication.doi_link, "http://dx.doi/org/10.1126/stke.2422004re10")                       
                    
class AuthorDetailsModelTests(TestCase):
    '''This class tests varios aspects of the `::class:AuthorDetails` model.'''
    fixtures = ['fixture_personnel']

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
        '''This test creates a `::class:AuthorDetails` with the required information only.'''
        test_authordetail = AuthorDetails(author=Personnel.objects.get(pk=1), 
            order = 1)
        test_authordetail.save() 
        
    def test_create_new_authordetail_all(self):
        '''This test creates a `::class:AuthorDetails` with the required information only.'''
        test_authordetail = AuthorDetails(author=Personnel.objects.get(pk=1), 
            order = 1,
            corresponding_author = True,
            equal_contribution = True)
        test_authordetail.save()             
            
    def test_authordetail_unicode(self):
        '''This tests that the unicode representaton of an authordetail is correct.'''
        test_authordetail = AuthorDetails(author=Personnel.objects.get(pk=1), 
            order = 1)
        test_authordetail.save() 
        self.AssertEqual(test_authordetail.__unicode__(), 'John Doe')