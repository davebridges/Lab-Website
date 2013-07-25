'''This package has the url encodings for the :mod:`papers` app.'''

from django.conf.urls import patterns, include, url

from papers import views

urlpatterns = patterns('',
    url(r'^interesting/?$', views.InterestingPaperList.as_view(), name="interesting-papers"), 
    url(r'^new/?$', views.PaperCreate.as_view(), name="paper-new"),
    url(r'^commentary/?$', views.CommentaryList.as_view(), name='commentary-list'),     
    url(r'^commentary/new/?$', views.CommentaryCreate.as_view(), name='commentary-new'),
    url(r'^commentary/(?P<pk>[-\d]+)/edit/?$', views.CommentaryUpdate.as_view(), name='commentary-edit'),
    url(r'^commentary/(?P<pk>[-\d]+)/delete/?$', views.CommentaryDelete.as_view(), name='commentary-delete'),
    url(r'^commentary/(?P<pk>[-\d]+)/?$', views.CommentaryDetail.as_view(), name='commentary-detail'),
    url(r'^(?P<title_slug>[-\w\d]+)/edit/?$', views.PaperUpdate.as_view(), name="paper-edit"),  
    url(r'^(?P<title_slug>[-\w\d]+)/delete/?$', views.PaperDelete.as_view(), name="paper-delete"),    
    url(r'^(?P<title_slug>[-\w\d]+)/?$', views.PaperDetailView.as_view(), name="paper-details"),                    
    url(r'^$', views.LaboratoryPaperList.as_view(), name="laboratory-papers"), 
)
