"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from personnel.models import LabMember

MODELS = [LabMember]

class LabMemberModelTests(TestCase):
    """Tests the model attributes of ::class:`LabMember` objects contained in the ::mod:`personnel` app."""


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
    
    def test_create_labmember_minimal(self):
        """This is a test for creating a new ::class:`LabMember`. object, with only the minimum fields being entered"""
        test_labmember = LabMember(first_name = 'joe',
        	last_name = 'blow',
        	email = 'joe@blow.com')
        test_labmember.save()
        self.assertEquals(test_labmember.id, 1)
        test that the slugfiy function works correctly
        self.assertEquals(test_labmember.name_slug, u'joe-blow')
