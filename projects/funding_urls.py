'''This package has the url encodings for the :mod:`funding` model.'''

from django.conf.urls import patterns, include, url

from projects import views

urlpatterns = patterns('',
    url(r'^new/?$', views.FundingCreate.as_view(), name="funding-new"),     
    url(r'^(?P<title_slug>[-\w\d]+)/edit/?$', views.FundingUpdate.as_view(), name="funding-edit"),  
    url(r'^(?P<title_slug>[-\w\d]+)/delete/?$', views.FundingDelete.as_view(), name="funding-delete"),    
    url(r'^(?P<title_slug>[-\w\d]+)/?$', views.FundingDetailView.as_view(), name="funding-details"),                    
    url(r'^$', views.FundingList.as_view(), name="funding-list"), 
)
