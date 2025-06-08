'''This package has the url encodings for the :mod:`papers` app.'''

from django.urls import path, re_path
from papers import views

urlpatterns = [
    path('interesting/', views.InterestingPaperList.as_view(), name="interesting-papers"),
    path('new/', views.PaperCreate.as_view(), name="paper-new"),
    # path('journal-club/', views.JournalClubList.as_view(), name="jc-list"),
    path('commentaries/', views.CommentaryList.as_view(), name='commentary-list'),
    path('commentary/', views.CommentaryList.as_view(), name='commentary-list'),
    path('commentary/new/', views.CommentaryCreate.as_view(), name='commentary-new'),
    re_path(r'^commentary/(?P<pk>[-\d]+)/edit/$', views.CommentaryUpdate.as_view(), name='commentary-edit'),
    re_path(r'^commentary/(?P<pk>[-\d]+)/delete/$', views.CommentaryDelete.as_view(), name='commentary-delete'),
    re_path(r'^commentary/(?P<pk>[-\d]+)/$', views.CommentaryDetail.as_view(), name='commentary-detail'),
    re_path(r'^(?P<title_slug>[-\w\d]+)/edit/$', views.PaperUpdate.as_view(), name="paper-edit"),
    re_path(r'^(?P<title_slug>[-\w\d]+)/delete/$', views.PaperDelete.as_view(), name="paper-delete"),
    re_path(r'^(?P<title_slug>[-\w\d]+)/$', views.PaperDetailView.as_view(), name="paper-details"),
    path('', views.LaboratoryPaperList.as_view(), name="laboratory-papers"),
]
