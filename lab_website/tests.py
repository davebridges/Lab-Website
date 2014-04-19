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
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()