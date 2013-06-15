'''This package has the url encodings for the communication app.'''

from django.conf.urls import patterns, include, url

from communication import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^twitter/?$', views.TwitterView.as_view(), name="twitter"),
    url(r'^calendar/?$', views.GoogleCalendarView.as_view(), name="google-calendar"),
    url(r'^wikipedia/?$', views.WikipedaEditsView.as_view(), name="wikipedia"),
    url(r'^lab-rules/?$', views.LabRulesView.as_view(), name="lab-rules"),
    url(r'^news/?$', views.NewsView.as_view(), name='lab-news'),
    url(r'/?$', views.ContactView.as_view(), name='contact-info'),
)
