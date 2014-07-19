'''This file is the model configuration file for the :mod`projects` app.

There is one model in this app, :class:`~projects.models.Project`.
'''

from django.db import models
from django.template.defaultfilters import slugify

from personnel.models import Person
from papers.models import Publication

class Project(models.Model):
    '''This model covers :class:`~projects.models.Projects`.
    
    The only required field is the title.
    There are optional fields for the priority, a summary, the start date, and links to our and other Publications,  current and previous Personnel
    '''
    
    title = models.CharField(max_length=150,
        help_text="Name of the Project.")
    title_slug = models.SlugField(blank=True, 
        null=True, 
        max_length=150, 
        editable=False, 
        unique=True)
        
    current_personnel = models.ManyToManyField(Person, 
        blank=True, 
        null=True, 
        help_text="Who is currently working on this project?",
        related_name = 'current_personnel')
    past_personnel = models.ManyToManyField(Person, 
        blank=True, 
        null=True,
        help_text="Who previously worked on this project?",
        related_name = 'previous_personnel')   
             
    summary = models.TextField(blank=True, null=True)
    start_date = models.DateField(help_text="When did we start this project",
        blank=True, 
        null=True)
    priority = models.IntegerField(blank=True, 
        null=True,
        help_text="Priority Rank, 1 is high, 5 is low")     
    
    publications = models.ManyToManyField(Publication,
        blank=True,
        null=True,
        help_text = "What papers have we written for this project?",
        related_name="publications")
    other_publications = models.ManyToManyField(Publication,
        blank=True,
        null=True,
        help_text = "What key papers have others written about this project?",
        related_name ="other_publications") 
           
    #these fields are automatically generated.    
    date_last_modified = models.DateField(auto_now=True)
    date_added = models.DateField(auto_now_add=True)      
    
    def __unicode__(self):
        '''The unicode representation for a :class:`~projects.models.Project` is its title'''
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        '''the permalink for a project detail page is **/projects/<title_slug>**'''
        return ('project-details', [str(self.title_slug)])   

    def save(self, *args, **kwargs):
        '''The title is slugified upon saving into title_slug.'''
        if not self.id:
            self.title_slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)
        
    class Meta:
        '''The meta options for the :class:`projects.models.Project` model is ordering set by priority then secondarily by the date_last_modified.'''
        ordering = ['priority','date_last_modified']
        
class Funding(models.Model):
    '''This model covers sources of funding, including grants and fellowships.
    
    The required field is the title'''
    
    title = models.CharField(help_text="The title of the awarded grant",
        max_length=200)
    title_slug = models.SlugField(blank=True, 
        null=True,
        editable=False, 
        max_length=150)
    amount = models.IntegerField(help_text="The total value of the award",
        blank=True,
        null=True)
    funding_agency = models.ForeignKey('FundingAgency',
        help_text="What was the funding agency",
        blank=True,
        null=True)
    start_date = models.DateField(help_text="The start date of this award",
        blank=True, 
        null=True)
    end_date = models.DateField(help_text="When this award ends",
        blank=True, 
        null=True)
    summary = models.TextField(help_text="The abstract of the award",
        blank=True,
        null=True)
    full_text = models.TextField(help_text="HTML Formatted full text",
        blank=True,
        null=True)
    publications = models.ManyToManyField(Publication,
        help_text="Which publications are associated with this award?",
        blank=True,
        null=True)
    projects = models.ManyToManyField(Project,
        help_text="Which projects are associated with this award?",
        blank=True,
        null=True)   
    active = models.BooleanField(help_text="Is this funding active?")
        
    #these fields are automatically generated.    
    date_last_modified = models.DateField(auto_now=True)
    date_added = models.DateField(auto_now_add=True)            
        
    def __unicode__(self):
        '''The unicode representation for a :class:`~projects.models.Funding` is its title'''
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        '''the permalink for a funding detail page is **/funding/<title_slug>**'''
        return ('funding-details', [str(self.title_slug)])   

    def save(self, *args, **kwargs):
        '''The title is slugified upon saving into title_slug.'''
        if not self.id:
            self.title_slug = slugify(self.title)
        super(Funding, self).save(*args, **kwargs)
        
class FundingAgency(models.Model):
    '''This model describes the funding agency.
    
    The required field for a funding agency is its name.'''
    
    name = models.CharField(help_text="The name of the funding agency", 
        max_length=100)
    short_name = models.CharField(help_text="A shortened name (ie NIH)",
        max_length=10,
        blank=True,
        null=True)
    website = models.URLField(help_text="The URL of the funding agency",
        blank=True,
        null=True)
    logo = models.ImageField(upload_to='funding_agency/%Y/%m/%d', 
        help_text="A logo for this funding agency",
        blank=True,
        null=True)
        
    def __unicode__(self):
        '''The unicode representation for a :class:`~projects.models.FundingAgency` is its name'''
        return self.name
