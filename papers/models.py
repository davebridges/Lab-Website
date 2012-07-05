from django.db import models
from django.template.defaultfilters import slugify

class Publication(models.Model):
    '''This model covers publications of several types.
    
    The publication fields are based on Mendeley and PubMed fields.
    ''''
    mendeley_url = models.URLField()
    title = models.CharField(max_length=150)
    title_slug = models.SlugField()
    id = models.IntegerField()
    doi = models.CharField(blank=True, null=True)
    year = models.IntegerField()
    issue = models.CharField(max_length=15)
    pages = models.CharField(max_length=15)
    abstract = models.TextField(max_length)
    
    def __unicode__(self):
        '''The unicode representation for a Publication is its title'''
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        '''the permalink for a paper detail page is /papers/[title_slug]'''
        return ('papers.views.paper-details', [str(self.title_slug)])   

    def save(self, *args, **kwargs):
        '''The title is slugified upon saving into title_slug.'''
        if not self.id:
            self.title_slug = slugify(self.title)
        super(Publication, self).save(*args, **kwargs)