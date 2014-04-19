'''This package has the url encodings for the :mod:`papers` app.'''

from django.conf.urls import patterns, include, url

from communication import views

urlpatterns = patterns('',
    url(r'^new/?$', views.PostCreate.as_view(), name="post-new"),
    url(r'^(?P<post_slug>[-\w\d]+)/edit/?$', 
        views.PostUpdate.as_view(), 
        name="post-edit"),  
    url(r'^(?P<post_slug>[-\w\d]+)/delete/?$', 
        views.PostDelete.as_view(), 
        name="post-delete"),    
    url(r'^(?P<post_slug>[-\w\d]+)/?$', 
        views.PostDetail.as_view(), 
        name="post-details"),                    
    url(r'^$', views.PostList.as_view(), name="post-list"), 
)
