from django.db import models
from django.template.defaultfilters import slugify

from personnel.models import Personnel

class Publication(models.Model):
    '''This model covers publications of several types.
    
    The publication fields are based on Mendeley and PubMed fields.
    For the author, there is a ManyToMany link to a group of authors with the order and other details.  See `::class:AuthorDetails`.
    '''
    mendeley_url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=150)
    authors = models.ManyToManyField(AuthorDetails, blank=True, null=True)
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
    
    def doi_link(self):
        '''This turns the DOI into a link.'''
        return 'http://dx.doi.org/%s' % self.doi
    
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
        
class AuthorDetails(models.Model):
    '''This is a group of authors for a specific paper.
        
    Because each `::class:Publicaiton` has a list of authors and the order matters, the authors are listed in this linked model.
    This model has a ManyToMany link with a paper as well as marks for order, and whether an author is a corresponding or equally contributing author.
    '''
    author = models.ForeignKey(Personnel)
    order = models.IntegerField(help_text='The order in which the author appears (do not duplicate numbers)')
    corresponding_author = models.BooleanField()
    equal_contributors = models.BooleanField(help_text='Check both equally contributing authors')
        
    def __unicode__(self):
        '''The unicode representation is the author name.'''
        return '%s' %self.author