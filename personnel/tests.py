"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import date

from personnel.models import Person, JobPosting, Organization, Role, JobType
from lab_website.tests import BasicTests

MODELS = [Person, JobPosting]

class PersonnelModelTests(BasicTests):
    """Tests the model attributes of ::class:`Personnel` objects contained in the ::mod:`personnel` app."""
    
    fixtures = ['test_personnel']
    
    def test_full_name(self):
        '''This is a test for the rendering of the full name from a ::class:`Person` object.'''
        fixture_personnel = Person.objects.get(first_name='John', last_name='Doe') 
        self.assertEqual(fixture_personnel.full_name(), 'John Doe')        
    
    def test_name_slug(self):
        '''This is a test for the rendering of the name_slug field from a ::class:`Person` object.'''
        fixture_personnel = Person.objects.get(first_name='John', last_name='Doe') 
        self.assertEqual(fixture_personnel.name_slug, 'john-doe')   

    def test_personnel_permalink(self):
        '''This is a test that the permalink for a ::class:`Person` object is correctly rendered as **/personnel/<name_slug>**'''
        fixture_personnel = Person.objects.get(first_name='John', last_name='Doe') 
        self.assertEqual(fixture_personnel.get_absolute_url(), '/people/john-doe/')          
    
    def test_create_labmember_minimal(self):
        '''This is a test for creating a new ::class:`Person` object, with only the minimum fields being entered'''
        test_labmember = Person(first_name = 'Joe',
        	last_name = 'Blow', alumni=False, current_lab_member=True)
        test_labmember.save()
        #test that the slugfiy function works correctly
        self.assertEqual(test_labmember.name_slug, 'joe-blow')

class JobTypeModelTests(BasicTests):

    fixtures = ['test_personnel.json', 'test_roles.json']
    
    def test_jobtype_str_representation(self):
        """Test string representation of JobType"""
        job_type = JobType.objects.create(
            job_title="Research Assistant",
            trainee_status=True,
            student_status=True,
            employee_status=False
        )
        self.assertEqual(str(job_type), "Research Assistant")
    
    def test_jobtype_creation_with_all_fields(self):
        """Test JobType creation with all boolean fields"""
        job_type = JobType.objects.create(
            job_title="Graduate Student",
            trainee_status=True,
            student_status=True,
            employee_status=False
        )
        self.assertEqual(job_type.job_title, "Graduate Student")
        self.assertTrue(job_type.trainee_status)
        self.assertTrue(job_type.student_status)
        self.assertFalse(job_type.employee_status)
    
    def test_jobtype_employee_status(self):
        """Test JobType for employee positions"""
        job_type = JobType.objects.create(
            job_title="Lab Manager",
            trainee_status=False,
            student_status=False,
            employee_status=True
        )
        self.assertEqual(str(job_type), "Lab Manager")
        self.assertFalse(job_type.trainee_status)
        self.assertFalse(job_type.student_status)
        self.assertTrue(job_type.employee_status)


class RoleModelTests(BasicTests):

    fixtures = ['test_personnel.json', 'test_roles.json']
    
    def setUp(self):
        """Set up test dependencies"""
        # Create test JobType
        self.job_type = JobType.objects.create(
            job_title="Research Assistant",
            trainee_status=True,
            student_status=True,
            employee_status=False
        )
        
        # Create test Organization
        self.organization = Organization.objects.create(name="Test University")
    
    def test_role_str_with_start_date_only(self):
        """Test string representation with only start date"""
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.organization,
            start_date=date(2023, 1, 15),
            end_date=None,
            public=True
        )
        expected = f"<strong>{self.job_type}</strong>, {self.organization} since 2023-01-15"
        self.assertEqual(str(role), expected)
    
    def test_role_str_with_end_date_only(self):
        """Test string representation with only end date"""
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.organization,
            start_date=None,
            end_date=date(2023, 12, 31),
            public=True
        )
        expected = f"<strong>{self.job_type}</strong>, {self.organization} until 2023-12-31"
        self.assertEqual(str(role), expected)
    
    def test_role_str_with_both_dates(self):
        """Test string representation with both start and end dates"""
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.organization,
            start_date=date(2023, 1, 15),
            end_date=date(2023, 12, 31),
            public=True
        )
        expected = f"<strong>{self.job_type}</strong>, {self.organization} from 2023-01-15 to 2023-12-31"
        self.assertEqual(str(role), expected)
    
    def test_role_str_with_no_dates(self):
        """Test string representation with no dates"""
        role = Role.objects.create(
            job_type=self.job_type,
            organization=self.organization,
            start_date=None,
            end_date=None,
            public=True
        )
        expected = f"<strong>{self.job_type}</strong>, {self.organization}"
        self.assertEqual(str(role), expected)            

class PersonnelViewTests(BasicTests):
    """Tests the views of ::class:`Personnel` objects contained in the ::mod:`personnel` app."""
    
    fixtures = ['test_personnel','test_address','test_labaddress']

    def test_fixture_loaded(self):
        people = Person.objects.filter(current_lab_member=True)
        self.assertTrue(people.exists())
    
    def test_laboratory_personnel(self):
        '''This function tests the laboratory-personnel view.''' 
        
        test_response = self.client.get('/people/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('personnel' in test_response.context)
        self.assertTemplateUsed(test_response, 'personnel_list.html')
        self.assertEqual(test_response.context['personnel_type'], 'current')
        self.assertEqual(test_response.context['personnel'][0].pk, 1)
        self.assertEqual(test_response.context['personnel'][0].first_name, 'John')        
        self.assertEqual(test_response.context['personnel'][0].last_name, 'Doe')  

    def test_personnel_detail(self):
        '''This function tests the personnel-details view.''' 
        
        test_response = self.client.get('/people/john-doe/')

        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('person' in test_response.context)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'personnel_detail.html')
        self.assertEqual(test_response.context['person'].pk, 1)
        self.assertEqual(test_response.context['person'].first_name, 'John')        
        self.assertEqual(test_response.context['person'].last_name, 'Doe')

          
class JobPostingModelTests(BasicTests):
    """Tests the model attributes of ::class:`JobPosting` objects contained in the ::mod:`personnel` app."""
   
    fixtures = ['test_organization',]

    def test_create_jobposting_minimal(self):
        '''This is a test for creating a new ::class:`JobPosting` object, with only the minimum fields being entered'''
        test_jobposting = JobPosting(title = 'Postdoctoral Researcher',
                              description = 'Some description',
                              link = 'http:/jobs.com/awesomejob',
                              active=True)
        test_jobposting.save()
        self.assertEqual(test_jobposting.pk, 1)    

    def test_create_jobposting_all(self):
        '''This is a test for creating a new ::class:`JobPosting` object, with only the minimum fields being entered'''
        test_jobposting = JobPosting(title = 'Postdoctoral Researcher',
                              description = 'Some description',
                              link = 'http:/jobs.com/awesomejob',
                              hiringOrganization = Organization.objects.get(pk=1),
                              education = "An educational requirement",
                              qualifications = "Some qualifications",
                              responsibilities = "Some responsibilities",
                              active = True)
        test_jobposting.save()
        self.assertEqual(test_jobposting.pk, 1)

    def test_jobposting_string(self):
        '''This test creates a new :class:`~personnel.models.JobPosting` object, then tests for the string representation of it.'''
        test_jobposting = JobPosting(title = 'Postdoctoral Researcher',
                              description = 'Some description',
                              link = 'http:/jobs.com/awesomejob',
                              active=True)
        test_jobposting.save()
        self.assertEqual(str(test_jobposting), 'Postdoctoral Researcher Job Posting (%s)' %(date.today()) )
