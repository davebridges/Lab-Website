'''This package has the url encodings for the :mod:`projects` app.'''

from django.urls import path, re_path
from projects import views

urlpatterns = [
    path('new/', views.ProjectCreate.as_view(), name="project-new"),
    re_path(r'^(?P<title_slug>[-\w\d]+)/edit/$', views.ProjectUpdate.as_view(), name="project-edit"),
    re_path(r'^(?P<title_slug>[-\w\d]+)/delete/$', views.ProjectDelete.as_view(), name="project-delete"),
    re_path(r'^(?P<title_slug>[-\w\d]+)/$', views.ProjectDetailView.as_view(), name="project-details"),
    path('', views.ProjectList.as_view(), name="project-list"),
]
