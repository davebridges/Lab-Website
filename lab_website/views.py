'''This package contains views for the root app.

So far this includes the home page.'''

import json
import urllib, urllib2

from django.conf import settings
from django.views.generic.base import View, TemplateView


class IndexView(TemplateView):
    '''This view redirects to the home page.'''
    
    template_name = "index.html"   
    
    def get_context_data(self, **kwargs):
        '''This function provides the context which is passed to this view.
        
        This will query facebook's pages API for simple information regarding the group.'''
        context = super(IndexView, self).get_context_data(**kwargs)
        
        def facebook_request(request_url):
            '''This function takes a request url and token and returns deserialized data.'''
            request = urllib2.Request(request_url)
            try:
                    response = urllib2.urlopen(request)
            except urllib2.URLError, e:
                    if e.code == 404:
                        data = "Facebook API is not Available."
                    else:
                        #this is for a non-404 URLError.
                        data = "Facebook API is not Available."
            except ValueError:
                    lab_rules = "Facebook API is not Available."        
            else:
                     #successful connection
                     json_data = response.read()
                     data = json.loads(json_data)
                     return data
         
        general_request_url = 'https://graph.facebook.com/' + settings.FACEBOOK_ID              
        context['general_data'] = facebook_request(general_request_url)
        milestone_request_url = 'https://graph.facebook.com/' + settings.FACEBOOK_ID +'/milestones?access_token=' + settings.FACEBOOK_ACCESS_TOKEN           
        context['milestones'] = facebook_request(milestone_request_url)
        posts_request_url = 'https://graph.facebook.com/' + settings.FACEBOOK_ID +'/posts?access_token=' + settings.FACEBOOK_ACCESS_TOKEN + '&limit=10'          
        context['posts'] = facebook_request(posts_request_url)        
        photos_request_url = 'https://graph.facebook.com/' + settings.FACEBOOK_ALBUM +'/photos?access_token=' + settings.FACEBOOK_ACCESS_TOKEN + '&limit=10'
        context['photo_url'] = photos_request_url          
        context['photos'] = facebook_request(photos_request_url)  
        return context                            