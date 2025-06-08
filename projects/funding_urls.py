"""URL patterns for the funding model in the projects app."""

from django.urls import path, re_path

from projects import views

urlpatterns = [
    path('new/', views.FundingCreate.as_view(), name="funding-new"),
    re_path(r'^(?P<title_slug>[-\w\d]+)/edit/$', views.FundingUpdate.as_view(), name="funding-edit"),
    re_path(r'^(?P<title_slug>[-\w\d]+)/delete/$', views.FundingDelete.as_view(), name="funding-delete"),
    re_path(r'^(?P<title_slug>[-\w\d]+)/$', views.FundingDetailView.as_view(), name="funding-details"),
    path('', views.FundingList.as_view(), name="funding-list"),
]
