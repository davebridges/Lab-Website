'''This module contains the models relevant to the :mod:`communication` app.

Currently there is just one model, for laboratory addresses.
'''

from django.db import models

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
        upload_to = '/location_images')
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