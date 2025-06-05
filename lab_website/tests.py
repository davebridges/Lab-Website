"""
This file contains the basic unit tests, which are imported into other apps.


"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from papers.models import Publication
from personnel.models import Person
from projects.models import Project

MODELS = [Publication, Person, Project]

class BasicTests(TestCase):
    '''This class covers the setup and tear down for all unit tests'''

    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login, 'Could not log in')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
class HomeViewTests(BasicTests):
    '''This class tests the views associated with the :mod:`communication` app.'''
    
    
    def test_feed_details_view(self):
        """This tests the feed-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        fixtures = ['test_labaddress']

        test_response = self.client.get('/')
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'index.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'facebook_api_sdk_script.html') 
        self.assertTemplateUsed(test_response, 'job_posting_snippet.html') 
        self.assertTemplateUsed(test_response, 'analytics_tracking.html') 
         #check that context processors are being passed                       
        self.assertTrue('lab_name' in test_response.context)
        self.assertTrue('twitter' in test_response.context)
        self.assertTrue('google_plus' in test_response.context)
        self.assertTrue('facebook' in test_response.context)
        self.assertTrue('disqus_forum' in test_response.context)        
        self.assertTrue('fb_app_id' in test_response.context)
        self.assertTrue('fb_admins' in test_response.context)
        self.assertTrue('analytics_tracking' in test_response.context)        
        self.assertTrue('analytics_root' in test_response.context)                          

