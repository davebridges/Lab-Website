'''This package contains models for the :mod:`personnel` app.'''

from django.db import models
from django.template.defaultfilters import slugify

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

class LabMember(models.Model):
    '''This class describes laboratory members.
    
    This class will include current and former laboratory members.
    
    The basis for this model is the http://schema.org/Person markup.'''
	#these fields are for identification
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    additional_names = models.CharField(max_length=100, null=True, blank=True, help_text='other (i.e. middle) names')
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    website = models.URLField(help_text='Personal Website', null=True, blank=True)
    #image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    degrees = models.ManyToManyField('Degree', help_text="Graduate and Undergraduate Degrees", blank=True, null=True)
    awards = models.ManyToManyField('Award', blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    home_address = models.ForeignKey('Address', blank=True, null=True, related_name='home-address')
    work_address = models.ForeignKey('Address', blank=True, null=True, related_name='work-address')
    #these fields describe the role while in the laboratory or either before/after their time there.
    lab_roles = models.ManyToManyField('Role', help_text="Position(s) in the laboratory", blank=True, null=True, related_name='lab-role')
    current_roles = models.ManyToManyField('Role', help_text="Current Position(s)", blank=True, null=True, related_name='current-role')
    past_roles = models.ManyToManyField('Role', help_text="Previous Position(s)", blank=True, null=True, related_name='past-role')
    #these fields describe updating information
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    name_slug = models.SlugField(unique=True, editable=False)
    
    def full_name(self):
        '''this function creates a full_name representation for both unicode and slug field displays.'''
        return "%s %s" %(self.first_name, self.last_name)
    
    def save(self, *args, **kwargs):
        '''Over-rides save to generate name_slug field.  This is only set upon creation to keep stability.'''
        if not self.id:
            self.name_slug = slugify(self.full_name)
        super(LabMember, self).save(*args, **kwargs)    
         
class Role(models.Model):
    ''''This model describes the type of job a ::class`LabMember` had.
    
    A laboratory member could have one or more Roles over time.'''
    job_type = models.ForeignKey('JobType', max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    graduation_status = models.NullBooleanField(help_text='It this was a student role, did this person graduate?')
    graduation_date = models.DateField(blank=True, null=True)
    degree = models.ManyToManyField('Degree', blank=True, null=True)  
    organization = models.ForeignKey('Organization')
    public = models.BooleanField(help_text='Should this role be displayed publicly?')
    
class JobType(models.Model):
    '''This model describes specific jobs.
    
    These can be current jobs, previous jobs or jobs while in the laboratory.
    This class describes jobs generically.  For details on a specific job see the associated ::class:`Role`.'''
    job_title = models.CharField(max_length=100)
    trainee_status = models.BooleanField(help_text='Is this person a trainee?', verbose_name="Trainee?")    
    student_status = models.BooleanField(help_text='Is this person a student?', verbose_name="Student?")    
    employee_status = models.BooleanField(help_text='Is this person an employee?', verbose_name="Employee?")
        
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
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(choices=ORGANIZATION_TYPE_CHOICES, max_length=100)  
    
class Address(models.Model):
    '''This class describes an address.'''
    line_1 = models.CharField(max_length=100, blank=True, null=True)
    line_2 = models.CharField(max_length=100, blank=True, null=True)
    line_3 = models.CharField(max_length=100, blank=True, null=True)
    line_4 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=3, help_text="Use 2 letter abbreviations", blank=True, null=True)
    country = models.CharField(max_length=100, help_text="Use standard country codes, see <a href="">here<a>.")
    code = models.CharField(max_length=15, blank=True, null=True)