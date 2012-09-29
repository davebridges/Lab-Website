'''This package has the url encodings for the :mod:`papers` app.'''

from django.conf.urls import patterns, include, url

from papers import views

urlpatterns = patterns('',
    url(r'^interesting/?$', views.InterestingPaperList.as_view(), name="interesting-papers"), 
    url(r'^new/?$', views.PaperCreate.as_view(), name="paper-new"),     
    url(r'^(?P<title_slug>[-\w\d]+)/edit/?$', views.PaperUpdate.as_view(), name="paper-edit"),  
    url(r'^(?P<title_slug>[-\w\d]+)/delete/?$', views.PaperDelete.as_view(), name="paper-delete"),    
    url(r'^(?P<title_slug>[-\w\d]+)/?$', views.PaperDetailView.as_view(), name="paper-details"),                    
    url(r'^$', views.LaboratoryPaperList.as_view(), name="laboratory-papers"), 
)
