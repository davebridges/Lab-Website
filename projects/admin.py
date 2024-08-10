'''This package sets up the admin interface for the :mod:`papers` app.'''
from django.contrib import admin
from projects.models import Funding, FundingAgency, Project

class FundingAdmin(admin.ModelAdmin):
    '''The :class:`~projects.models.Funding` model admin is the default.'''    
    pass
admin.site.register(Funding, FundingAdmin)

class FundingAgencyAdmin(admin.ModelAdmin):    
    '''The :class:`~projects.models.FundingAgency` model admin is the default.'''
    pass
admin.site.register(FundingAgency, FundingAgencyAdmin)

class ProjectAdmin(admin.ModelAdmin):
    '''The :class:`~projects.models.Project` model admin is the default.'''
    pass
admin.site.register(Project, ProjectAdmin)
