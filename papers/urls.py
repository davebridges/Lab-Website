'''This package has the url encodings for the papers app.'''

from django.conf.urls import patterns, include, url

from papers import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.LaboratoryPaperList.as_view(), name="laboratory-papers"), 
    url(r'^interesting/$', views.InterestingPaperList.as_view(), name="interesting-papers"), 
    url(r'^(?P<title_slug>[-\w]+)/$', views.PaperDetailView.as_view(), name="paper-details"),     
)
