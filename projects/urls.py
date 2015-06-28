'''This package has the url encodings for the :mod:`projects` app.'''

from django.conf.urls import patterns, include, url

from projects import views

urlpatterns = patterns('',
    url(r'^new/?$', views.ProjectCreate.as_view(), name="project-new"),     
    url(r'^(?P<title_slug>[-\w\d]+)/edit/?$', views.ProjectUpdate.as_view(), name="project-edit"),  
    url(r'^(?P<title_slug>[-\w\d]+)/delete/?$', views.ProjectDelete.as_view(), name="project-delete"),    
    url(r'^(?P<title_slug>[-\w\d]+)/?$', views.ProjectDetailView.as_view(), name="project-details"),                    
    url(r'^/?$', views.ProjectList.as_view(), name="project-list"), 
)
