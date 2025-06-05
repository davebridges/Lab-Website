'''This file is the model configuration file for the :mod`papers` app.

There are two models in this app, :class:`~papers.models.Publication` and :class:`~papers.models.AuthorDetails`
'''

from django.db import models
from django.template.defaultfilters import slugify

from personnel.models import Person

#Publication types are based on http://apidocs.mendeley.com/home/documenttypes
PUBLICATION_TYPES = (
	('Most Common', (
			('journal-article','Journal Article'),
			('book-section', 'Book Section'),
			)
	),
	('Less Common', (		
		('bill', 'Bill'),
		('book', 'Book'),
		('case', 'Case'),
		('computer-program', 'Computer Program'),
		('conference-proceedings', 'Conference Proceedings'),
		('encyclopedia-article', 'Encyclopedia Article'),
		('film', 'Film'),
		('generic', 'Generic'),
		('magazine-article','Magazine Article'),
		('newspaper-article','Newspaper Article'),
		('patent', 'Patent'),
		('report','Report'),
		('statute', 'Statute'),
		('television-broadcast', 'Television Broadcast'),
		('web-page', 'Web Page'),
		)
	),
)

class Publication(models.Model):
    '''This model covers :class:`~papers.models.Publication` objects of several types.
    
    The publication fields are based on Mendeley and PubMed fields.
    For the author, there is a ManyToMany link to a group of authors with the order and other details, see :class:`~papers.models.AuthorDetails`.
    '''
    mendeley_url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField('AuthorDetails', blank=True)
    title_slug = models.SlugField(blank=True, null=True, max_length=150, editable=False, unique=True)
    mendeley_id = models.IntegerField(blank=True, null=True)
    doi = models.CharField(blank=True, null=True, max_length=50, help_text="Digital Object Identifier", verbose_name="DOI")
    pmid = models.IntegerField(blank=True, null=True, help_text='PubMed Idenfifier', verbose_name="PMID")
    pmcid = models.IntegerField(blank=True, null=True, help_text='PubMed Central Idenfifier', verbose_name="PMCID")    
    journal = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    volume = models.CharField(max_length=15, blank=True, null=True)    
    issue = models.CharField(max_length=15, blank=True, null=True)
    pages = models.CharField(max_length=15, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    type = models.CharField(choices = PUBLICATION_TYPES, max_length=20, blank=True, null=True)
    laboratory_paper = models.BooleanField(help_text="Is this paper from our lab?")
    interesting_paper = models.BooleanField(help_text="Is this paper of interest but from another lab?")
    publication_date = models.DateField(help_text="The official publicaiton date of the paper", blank=True, null=True)
    preprint = models.BooleanField(help_text="Is this a preprint")
    date_last_modified = models.DateField(auto_now=True)
    date_added = models.DateField(auto_now_add=True)    
    
    def doi_link(self):
        '''This turns the DOI into a link.'''
        return 'http://dx.doi.org/%s' % self.doi
        
    def full_pmcid(self):
        '''Converts the integer to a full PMCID'''
        return 'PMC%s' % self.pmcid 
        
    def link(self):
        '''This generates the internal link to the paper.  The priority is the DOI, followed by the PMID, followed by our internal page.'''
        if self.doi:
            return self.doi_link()
        elif self.pmid:
            return 'http://pubmed.org/%s' % self.pmid
        else:
            return self.get_absolute_url()       
    
    def __unicode__(self):
        '''The unicode representation for a :class:`~papers.models.Publication` is its title'''
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        '''the permalink for a paper detail page is **/papers/<title_slug>**'''
        return ('paper-details', [str(self.title_slug)])   

    def save(self, *args, **kwargs):
        '''The title is slugified upon saving into title_slug.'''
        if not self.id:
            self.title_slug = slugify(self.title)
        super(Publication, self).save(*args, **kwargs)
        
    class Meta:
        '''The meta options for the :class:`papers.models.Publicaiton` model is ordering set by publication year then secondarily by the date the publication was added to the database.'''
        ordering = ['-publication_date', '-year', 'date_added']
        
        
class AuthorDetails(models.Model):
    '''This is a group of authors for a specific paper.
        
    Because each :class:`~papers.models.Publication` has a list of authors and the order matters, the authors are listed in this linked model.
    The authors are defined by the :class:`~personnel.models.Person` model class, which is also the UserProfile class.
    This model has a ManyToMany link with a paper as well as marks for order, and whether an author is a corresponding or equally contributing author.
    '''
    author = models.ForeignKey('personnel.Person')
    order = models.IntegerField(help_text='The order in which the author appears (do not duplicate numbers)')
    corresponding_author = models.BooleanField()
    equal_contributors = models.BooleanField(help_text='Check both equally contributing authors')
    contribution = models.ManyToManyField('AuthorContributions',
        help_text="Author contribution",
        blank=True)
                
    def __unicode__(self):
        '''The unicode representation is the author name.'''
        return '%i - %s -  %s' %(self.order, self.publication_set.last(), self.author)
    
    def name(self):
        '''The name representation shows the author name only.'''
        return '%s' %str(self.author)
    
    class Meta:
        '''The meta options set this field to be ordered based on order and sets the verbose name.'''
        verbose_name_plural = "author details"
        ordering = ['-publication__publication_date', ]

class Commentary(models.Model):
    '''This is a commentary by someone in our group on a paper we have discussed.

    The requires fields are the :class:`~papers.models.Paper`, and the comments. The author (:class:`~personnel.models.Person`) and the citation are optional.
    There are autopopulated fields for creation and updates.
    '''
    author = models.ForeignKey('personnel.Person', 
        blank=True, null=True,
        help_text="Who was the primary author of this commentary?")
    paper = models.ForeignKey('Publication')
    comments = models.TextField(help_text="Comments on this paper")
    citation = models.TextField(blank=True, null=True,
                 help_text="Generate citation at http://scienceseeker.org/generate-citations")

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __unicode__(self):
        '''The unicode representation is "Commentary on XXX" where XXX is the paper title'''
        return "Journal club summary on %s" %self.paper

    @models.permalink
    def get_absolute_url(self):
        '''The permalink of a commentary oage is **commentaries/<pk>**'''
        return('commentary-detail', [str(self.id)])

    class Meta:
        '''The meta options for this defines the ordering by the created field.'''
        ordering = ['-created',]

class JournalClubArticle(models.Model):
    '''This is a brief list of articles discussed in journal club.

    The only required field is the citation.
    Optional fields include date, DOI and commentary'''

    citation = models.TextField(help_text="Formatted citation, based on Scientific Reports")
    
    presentation_date = models.DateField(blank=True, null=True)
    doi = models.CharField(blank=True, null=True, max_length=50, help_text="Digital Object Identifier", verbose_name="DOI")
    commentary = models.ForeignKey('Commentary', blank=True, null=True, help_text="Did we write comments on this paper?")

    def doi_link(self):
        '''This turns the DOI into a link.'''
        return 'http://dx.doi.org/%s' % self.doi

    def get_absolute_url(self):
        '''This turns the DOI into a link.'''
        return '//dx.doi.org/%s' % self.doi

    class Meta:
        '''The meta options for this defines the ordering by the created field.'''
        ordering = ['-presentation_date',]  
        
    def __unicode__(self):
        '''The unicode representation is "Commentary on XXX" where XXX is the paper title'''
        return "Journal club article: %s" %self.citation     

class AuthorContributions(models.Model):
    '''This is an ontology that describes the actual contribution of an author.
    
    This is an empty dataset but will be populated by the CRediT ontology types and images (see http://dictionary.casrai.org/Contributor_Roles/ for the ontology)
    Badge images need to be added manually'''
    
    contribution = models.CharField(help_text='Short name of the contirbution',blank=True, null=True, max_length=100)
    url = models.URLField(help_text='URL for the ontology', blank=True, null=True)
    image = models.ImageField(
        upload_to='contributor-badges', 
        help_text="Badge for this contribution",
        blank=True,
        null=True)
    image_url = models.URLField(help_text="URL for the badge", blank=True, null=True)
    description = models.TextField(
        help_text="Details on what exactly is meant by this contribution",
        blank=True,
        null=True)
        
    def __unicode__(self):
        '''The unicode representation is the contribution'''
        return self.contribution
