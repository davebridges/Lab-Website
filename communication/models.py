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