'''This module contains the models relevant to the :mod:`communication` app.

Currently there is just one model, for laboratory addresses.
'''

from django.db import models
from django.template.defaultfilters import slugify

from personnel.models import Address

class LabAddress(models.Model):
    '''This object indicates contact information for the lab.
    
    This is used to give several types of addresses.'''
    
    ADDRESS_TYPES = (
        ('Primary', 'Primary Address'),
        ('Secondary', 'Secondary Address'),
        ('Shipping', 'Shipping Address'))
        
    type = models.CharField(max_length=15,
        help_text="What type of address is this?",
        choices = ADDRESS_TYPES)
    address = models.ForeignKey(Address, help_text = 'What is the address?"')
    
    def __unicode__(self):
        '''The unicode representation of an address is the root address.'''
        return '%s' %self.address
        
class LabLocation(models.Model):
    '''This object stores general information about where the group is situated.
    
    This is a general model which can store information at a variety of levels, including the department, the institution or the city/region.
    There can be several instances of this for each group to describe various levels of location.
    There is are three required fields; name, type and priority.
    '''
    
    LOCATION_TYPE = (
        ('Department', 'Department'),
        ('Institution', 'Institution'),
        ('City', 'City'),
        ('Region', 'Region'))
        
    name = models.CharField(max_length=50,
        help_text = "What is the name of this location?")    
    type = models.CharField(max_length=15,
        help_text = "What type of location is this?",
        choices = LOCATION_TYPE)
    address = models.ForeignKey(Address,
        help_text = "What is the address for this location",
        blank = True, null = True)
    image = models.ImageField(help_text="A representative image of this location",
        blank=True, null=True,
        upload_to = 'location_images')
    url = models.URLField(help_text="What is the official link for this location?",
        blank=True, null = True)
    description = models.TextField(help_text="A description of thise place",
        blank=True, null=True)
    lattitude = models.FloatField(help_text="What is the lattitude of this location?",
        blank=True, null=True)
    longitude = models.FloatField(help_text="What is the longitude of this location?",
        blank=True, null=True)
    priority = models.IntegerField(help_text="What is the display priority for this location (1 is high, 5 is low)")
    
    def __unicode__(self):
        '''The unicode representation of an address is its name.'''
        return '%s' % self.name
        
    class Meta:
       '''These objects are ordered by their priority.'''
       
       ordering = ['priority',]
       
class Post(models.Model):
    '''This is a post by someone in our group on some topic.

    The required fields are the title, the author (:class:`~personnel.models.Person`) and the url where the raw markdown can be found.
    There are also required fields for creation and updates.
    The optional fields are a linked paper, and linked project.
    '''
    
    post_title = models.CharField(max_length=100, help_text="What is the title of this post?")
    post_slug = models.SlugField(blank=True, null=True, 
        max_length=100, editable=False, unique=True)
    author = models.ForeignKey('personnel.Person', 
        help_text="Who was the primary author of this post?")
    markdown_url = models.URLField(help_text="Where is the raw markdown file to be parsed?")
    
    paper = models.ForeignKey('papers.Publication', blank=True, null=True,
        help_text="Does this post refer to one of our papers?")
    project = models.ForeignKey('projects.Project', blank=True, null=True,
        help_text="Does this post refer to one of our projects?")


    created = models.DateField(auto_now_add=True)
    modified = models.DateField(blank=True, null=True)

    def __unicode__(self):
        '''The unicode representation is the post_title'''
        return "%s" %self.post_title

    @models.permalink
    def get_absolute_url(self):
        '''The permalink of a post page is **post/<post_slug>**'''
        return('post-detail', [str(self.post_slug)])

    class Meta:
        '''The meta options for this defines the ordering by the created field.'''
        ordering = ['-created',]   
        
    def save(self, *args, **kwargs):
        '''The post_title is slugified upon saving into post_slug.'''
        if not self.id:
            self.post_slug = slugify(self.post_title)
        super(Post, self).save(*args, **kwargs)         
       