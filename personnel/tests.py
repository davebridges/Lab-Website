"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from personnel.models import Person

MODELS = [Person]

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
        '''This is a test for the rendering of the full name from a ::class:`Person` object.'''
        fixture_personnel = Person.objects.get(first_name='John', last_name='Doe') 
        self.assertEquals(fixture_personnel.full_name(), 'John Doe')        
    
    def test_name_slug(self):
        '''This is a test for the rendering of the name_slug field from a ::class:`Person` object.'''
        fixture_personnel = Person.objects.get(first_name='John', last_name='Doe') 
        self.assertEquals(fixture_personnel.name_slug, 'john-doe')   

    def test_personnel_permalink(self):
        '''This is a test that the permalink for a ::class:`Person` object is correctly rendered as **/personnel/<name_slug>**'''
        fixture_personnel = Person.objects.get(first_name='John', last_name='Doe') 
        self.assertEquals(fixture_personnel.get_absolute_url(), '/people/john-doe/')          
    
    def test_create_labmember_minimal(self):
        '''This is a test for creating a new ::class:`Person` object, with only the minimum fields being entered'''
        test_labmember = Person(first_name = 'Joe',
        	last_name = 'Blow')
        test_labmember.save()
        #test that the slugfiy function works correctly
        self.assertEquals(test_labmember.name_slug, u'joe-blow')

class PersonnelViewTests(TestCase):
    """Tests the views of ::class:`Personnel` objects contained in the ::mod:`personnel` app."""
    
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
                
    def test_laboratory_personnel(self):
        '''This function tests the laboratory-personnel view.''' 
        
        test_response = self.client.get('/people/')

        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('personnel' in test_response.context)
        self.assertTemplateUsed(test_response, 'personnel_list.html')
        self.assertEqual(test_response.context['personnel-type'], 'current')
        self.assertEqual(test_response.context['personnel'][0].pk, 1)
        self.assertEqual(test_response.context['personnel'][0].first_name, 'John')        
        self.assertEqual(test_response.context['personnel'][0].last_name, 'Doe')  

    def test_personnel_detail(self):
        '''This function tests the personnel-details view.''' 
        
        test_response = self.client.get('/people/john-doe/')

        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('person' in test_response.context)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jquery_script.html')
        self.assertTemplateUsed(test_response, 'personnel_detail.html')
        self.assertEqual(test_response.context['person'].pk, 1)
        self.assertEqual(test_response.context['person'].first_name, 'John')        
        self.assertEqual(test_response.context['person'].last_name, 'Doe')          