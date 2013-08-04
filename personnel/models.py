'''This package contains models for the :mod:`personnel` app.

Currently the models in this are:

* :class:`~personnel.models.Person`
* :class:`~personnel.models.Role`
* :class:`~personnel.models.JobType`
* :class:`~personnel.models.Degree`
* :class:`~personnel.models.Award`
* :class:`~personnel.models.Organization`
* :class:`~personnel.models.Address`
'''

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)   

ORGANIZATION_TYPE_CHOICES = (
	('Academic', 'Academic'),
	('Industry', 'Industry'),
	('Non-Profit', 'Non-Profit'),
	('Other', 'Other')
) 

class Person(models.Model):
    '''This class describes laboratory members.
    
    This class will include current and former laboratory members.
    There are no required fields since this object can be created with a User instance creation.  
    This is the UserProfile model and can be accessed from request.User.get_profile().
    The basis for this model is the http://schema.org/Person markup.
    Currently the image field for a person is a gravatar based on their email.'''
    
	#these fields are for identification
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    additional_names = models.CharField(max_length=100, null=True, blank=True, help_text='other (i.e. middle) names')
    email = models.EmailField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True, help_text="Personal Biography.")
    phone = models.CharField(max_length=40, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    website = models.URLField(help_text='Personal Website', null=True, blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', 
        blank=True, 
        null=True)
    degrees = models.ManyToManyField('Degree', help_text="Graduate and Undergraduate Degrees", blank=True, null=True)
    awards = models.ManyToManyField('Award', blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    home_address = models.ForeignKey('Address', blank=True, null=True, related_name='home-address')
    work_address = models.ForeignKey('Address', blank=True, null=True, related_name='work-address')
    #these fields describe social networking usernames or id numbers
    google_plus_user_id = models.CharField(max_length=25, blank=True, null=True, verbose_name="Google Plus Id")
    twitter_username = models.CharField(max_length=15, blank=True, null=True)
    facebook_user_id = models.CharField(max_length=15, blank=True, null=True)
    #these fields describe the role while in the laboratory or either before/after their time there.
    current_lab_member = models.BooleanField()
    lab_roles = models.ManyToManyField('Role', help_text="Position(s) in the laboratory", blank=True, null=True, related_name='lab-role')
    current_roles = models.ManyToManyField('Role', help_text="Current Position(s)", blank=True, null=True, related_name='current-role')
    past_roles = models.ManyToManyField('Role', help_text="Previous Position(s)", blank=True, null=True, related_name='past-role')
    #these fields describe updating information and are automatically filled
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    name_slug = models.SlugField(editable=False)
    user = models.OneToOneField(User, blank=True, null=True, help_text="Username for this person")
    
    def __unicode__(self):
        '''The unicode representation for a Personnel object is its full name'''
        return self.full_name()
        
    @models.permalink
    def get_absolute_url(self):
        '''the permalink for a paper detail page is /personnel/[name_slug]'''
        return ('personnel-details', [str(self.name_slug)])   
    
    def full_name(self):
        '''this function creates a full_name representation for both unicode and slug field displays.'''
        if self.last_name is None:
            return "No Name Given"
        else:
            return "%s %s" %(self.first_name, self.last_name)
    
    def save(self, *args, **kwargs):
        '''Over-rides save to generate name_slug field.  This is only set upon creation to keep stability.'''
        if not self.id:
            self.name_slug = slugify(self.full_name())
        super(Person, self).save(*args, **kwargs) 

    class Meta:
        '''The meta options for Personnel models.'''
        ordering = ["last_name"]
        verbose_name_plural = "Personnel"
        
def create_user_profile(sender, instance, created, **kwargs):
    '''This function creates a Person object for each user.'''
    if created:
        Person.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)        
         
class Role(models.Model):
    ''''This model describes the type of job a ::class`LabMember` had.
    
    A laboratory member could have one or more Roles over time.'''
    job_type = models.ForeignKey('JobType', max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    graduation_status = models.NullBooleanField(help_text='It this was a student role, did this person graduate?')
    graduation_date = models.DateField(blank=True, null=True)
    degree = models.ManyToManyField('Degree', blank=True, null=True)  
    organization = models.ForeignKey('Organization')
    public = models.BooleanField(help_text='Should this role be displayed publicly?')
    
    def __unicode__(self):
        '''The unicode representation for a Role object is the jobtype'''
        return u"<strong>%s</strong>, %s" %(self.job_type, self.organization)
    
class JobType(models.Model):
    '''This model describes specific jobs.
    
    These can be current jobs, previous jobs or jobs while in the laboratory.
    This class describes jobs generically.  For details on a specific job see the associated ::class:`Role`.'''
    job_title = models.CharField(max_length=100)
    trainee_status = models.BooleanField(help_text='Is this person a trainee?', verbose_name="Trainee?")    
    student_status = models.BooleanField(help_text='Is this person a student?', verbose_name="Student?")    
    employee_status = models.BooleanField(help_text='Is this person an employee?', verbose_name="Employee?")
    
    def __unicode__(self):
        '''The unicode representation for a JobType object is the title'''
        return u'%s' %self.job_title
        
class Degree(models.Model):
    '''This model describes degrees, undergraduate and graduate.
    
    These describe degrees in general.  For details on a specific degree see the associated ::class:`Role`.'''
    degree = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)

class Award(models.Model):
    '''This model describes awards that lab personnel has won.'''
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField(blank=True, null=True)
    organization = models.ForeignKey('Organization')
    
class Organization(models.Model):
    '''This class describes an business, institution or other organization.'''   
    name = models.CharField(max_length=100, 
        unique=True, 
        help_text="Name of the University or Institute")
    department = models.CharField(max_length=100,
        help_text="Name of the Department or Group")
    type = models.CharField(choices=ORGANIZATION_TYPE_CHOICES, max_length=100)
    
    def __unicode__(self):
        '''The unicode representation for an Organization object is the department and the institution separated by a linebreak'''
        return u'%s, %s' %(self.department, self.name,)
    
class Address(models.Model):
    '''This class describes an address.'''
    line_1 = models.CharField(max_length=100, blank=True, null=True)
    line_2 = models.CharField(max_length=100, blank=True, null=True)
    line_3 = models.CharField(max_length=100, blank=True, null=True)
    line_4 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=3, help_text="Use 2 letter abbreviations", blank=True, null=True)
    country = models.CharField(max_length=100, help_text="Use standard country codes, see <a href="">here<a>.")
    code = models.CharField(max_length=15, blank=True, null=True, help_text="zip or postal code")
    
    def __unicode__(self):
        '''The unicode representation of an Address is the address lines followed by linebreaks.'''
        return u'%s\n%s\n%s\n%s\n%s, %s, %s, %s' %(self.line_1, self.line_2, self.line_3, self.line_4, self.city, self.state, self.country, self.code)


class JobPosting(models.Model):
    '''This class describes a job posting.

    It includes the description, an active checkbox and a link to where to apply.
    '''

    title = models.CharField(max_length=30, help_text="The official position title")
    description = models.TextField(help_text="Describe the available position")
    link = models.URLField(help_text="Link to application")

    #job details
    hiringOrganization = models.ForeignKey('Organization', blank=True, null=True)
    education = models.TextField(help_text="Minimum educational requirements", blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    active = models.BooleanField(help_text="Is this posting currently active")

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __unicode__(self):
        '''The unicode representation is the created field.'''
        return u'%s Job Posting (%s)' %(self.title, self.created)
