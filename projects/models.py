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
        related_name="publications_set")
    other_publications = models.ManyToManyField(Publication,
        blank=True,
        null=True,
        help_text = "What key papers have others written about this project?",
        related_name ="other_publications_set") 
           
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