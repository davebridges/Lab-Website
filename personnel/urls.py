'''This package has the url encodings for the personnel app.'''

from django.urls import path, re_path
from personnel import views

urlpatterns = [
    path('', views.LaboratoryPersonnelList.as_view(), name="laboratory-personnel"),
    path('alumni/', views.LaboratoryAlumniList.as_view(), name="laboratory-alumni"),
    re_path(r'^(?P<name_slug>[\w\d-]+)/$', views.LaboratoryPersonnelDetail.as_view(), name="personnel-details"),
]
