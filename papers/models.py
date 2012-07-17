from django.db import models
from django.template.defaultfilters import slugify

from personnel.models import Personnel

class Publication(models.Model):
    '''This model covers publications of several types.
    
    The publication fields are based on Mendeley and PubMed fields.
    '''
    mendeley_url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=150)
    authors = models.ManyToManyField(Personnel, blank=True, null=True)
    title_slug = models.SlugField(blank=True, null=True, max_length=150)
    mendeley_id = models.IntegerField(blank=True, null=True)
    doi = models.CharField(blank=True, null=True, max_length=50)
    pmid = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    issue = models.CharField(max_length=15, blank=True, null=True)
    pages = models.CharField(max_length=15, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    laboratory_paper = models.BooleanField(help_text="Is this paper from our lab?")
    interesting_paper = models.BooleanField(help_text="Is this paper of interest but from another lab?")
    date_last_modified = models.DateField(auto_now=True)
    date_added = models.DateField(auto_now_add=True)    
    
    def __unicode__(self):
        '''The unicode representation for a Publication is its title'''
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        '''the permalink for a paper detail page is /papers/[title_slug]'''
        return ('paper-details', [str(self.title_slug)])   

    def save(self, *args, **kwargs):
        '''The title is slugified upon saving into title_slug.'''
        if not self.id:
            self.title_slug = slugify(self.title)
        super(Publication, self).save(*args, **kwargs)