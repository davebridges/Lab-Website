'''This package has the url encodings for the :mod:`papers` app.'''

from django.urls import path, re_path
from communication import views

urlpatterns = [
    path('new/', views.PostCreate.as_view(), name="post-new"),
    re_path(r'^(?P<post_slug>[-\w\d]+)/edit/$', views.PostUpdate.as_view(), name="post-edit"),
    re_path(r'^(?P<post_slug>[-\w\d]+)/delete/$', views.PostDelete.as_view(), name="post-delete"),
    re_path(r'^(?P<post_slug>[-\w\d]+)/$', views.PostDetail.as_view(), name="post-details"),
    path('', views.PostList.as_view(), name="post-list"),
]

