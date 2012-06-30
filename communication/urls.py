'''This package has the url encodings for the urls app.'''

from django.conf.urls import patterns, include, url

from communication import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lab_website.views.home', name='home'),
    # url(r'^lab_website/', include('lab_website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^twitter/$', views.TwitterView.as_view(), name="twitter"),
    url(r'^calendar/$', views.GoogleCalendarView.as_view(), name="google-calendar"),
    url(r'^wikipedia/$', views.WikipedaEditsView.as_view(), name="wikipedia") 
)
