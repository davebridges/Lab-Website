"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from personnel.models import Personnel

MODELS = [Personnel]

class PersonnelModelTests(TestCase):
    """Tests the model attributes of ::class:`Personnel` objects contained in the ::mod:`personnel` app."""
    
    fixtures = ['test_personnel']

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
                
    def test_full_name(self):
        '''This is a test for the rendering of the full name from a ::class:`Personnel` object.'''
        fixture_personnel = Personnel.objects.get(first_name='John', last_name='Doe') 
        self.assertEquals(fixture_personnel.full_name(), 'John Doe')        
    
    def test_name_slug(self):
        '''This is a test for the rendering of the name_slug field from a ::class:`Personnel` object.'''
        fixture_personnel = Personnel.objects.get(first_name='John', last_name='Doe') 
        self.assertEquals(fixture_personnel.name_slug, 'john-doe')        
    
    def test_create_labmember_minimal(self):
        '''This is a test for creating a new ::class:`Personnel`. object, with only the minimum fields being entered'''
        test_labmember = Personnel(first_name = 'Joe',
        	last_name = 'Blow')
        test_labmember.save()
        #test that the slugfiy function works correctly
        self.assertEquals(test_labmember.name_slug, u'joe-blow')
