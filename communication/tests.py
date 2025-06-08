"""
This file contains the unit tests for the :mod:`communication` app.

Since this app has no models there is model and view tests:

* :class:`~communication.tests.CommunicationModelTests`
* :class:`~communication.tests.CommunicationViewTests` 

"""

from lab_website.tests import BasicTests

from communication.models import LabAddress,LabLocation,Post

from personnel.models import Address, Person
from papers.models import Publication
from projects.models import Project

class CommunicationModelTests(BasicTests):
    '''This class tests the views associated with models in the :mod:`communication` app.'''
    
    fixtures = ['test_address',]
    
    def test_create_new_lab_address(self):
        '''This test creates a :class:`~communication.models.LabAddress` with the required information.'''
 
        test_address = LabAddress(type='Primary', address=Address.objects.get(pk=1)) #repeat for all required fields
        test_address.save()
        self.assertEqual(test_address.pk, 1) #presumes no models loaded in fixture data     
        
    def test_lab_address_string(self):
        '''This tests the string representation of a :class:`~communication.models.LabAddress`.'''
 
        test_address = LabAddress(type='Primary', address=Address.objects.get(pk=1)) #repeat for all required fields
        test_address.save()
        self.assertEqual(test_address.pk, 1) #presumes no models loaded in fixture data  
        self.assertEqual(str(test_address), Address.objects.get(pk=1).__str__())
        
    def test_create_new_lab_location(self):
        '''This test creates a :class:`~communication.models.LabLocation` with the required information only.'''
 
        test_location = LabLocation(name = 'Memphis', 
            type='City', 
            priority=1) #repeat for all required fields
        test_location.save()
        self.assertEqual(test_location.pk, 1) #presumes no models loaded in fixture data         

    def test_create_new_lab_location_all(self):
        '''This test creates a :class:`~communication.models.LabLocation` with all fields included.'''
 
        test_location = LabLocation(name = 'Memphis', 
            type='City', 
            priority=1,
            address=Address.objects.get(pk=1),
            url = 'www.cityofmemphis.org',
            description = 'some description about the place',
            lattitude = 35.149534,
            longitude = -90.04898,) #repeat for all required fields
        test_location.save()
        self.assertEqual(test_location.pk, 1) #presumes no models loaded in fixture data
        
    def test_lab_location_string(self):
        '''This test creates a :class:`~communication.models.LabLocation` with the required information only.'''
 
        test_location = LabLocation(name = 'Memphis', 
            type='City', 
            priority=1) #repeat for all required fields
        test_location.save()
        self.assertEqual(test_location.pk, 1)
        self.assertEqual(str(test_location), 'Memphis') 

class CommunicationViewTests(BasicTests):
    '''This class tests the views associated with the :mod:`communication` app.'''
    
    
    def test_feed_details_view(self):
        """This tests the feed-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/feeds', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'feed_details.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('google_calendar_id' in test_response.context)          
        
    def test_lab_rules_view(self):
        '''This tests the lab-rules view.
        
        The tests ensure that the correct template is used.
        It also tests whether the correct context is passed (if included).
        his view uses a user with superuser permissions so does not test the permission levels for this view.'''
        
        test_response = self.client.get('/lab-rules', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'lab_rules.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('lab_rules' in test_response.context)    
        self.assertTrue('lab_rules_source' in test_response.context)    

    def test_lab_rules_view(self):
        '''This tests the data-resource-sharing view.
        
        The tests ensure that the correct template is used.
        It also tests whether the correct context is passed (if included).
        his view uses a user with superuser permissions so does not test the permission levels for this view.'''
        
        test_response = self.client.get('/data-resource-sharing', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'data_sharing_policy.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('data_sharing_policy' in test_response.context)    
        self.assertTrue('data_sharing_policy_source' in test_response.context)
        
    def test_twitter_view(self):
        '''This tests the twitter view.
        
        Currently it just ensures that the template is loading correctly.
        '''
        test_response = self.client.get('/twitter', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'twitter_timeline.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('timeline' in test_response.context)         
        
        
    def test_calendar_view(self):
        '''This tests the google-calendar view.
        
        Currently it just ensures that the template is loading correctly.
        '''
        test_response = self.client.get('/calendar', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'calendar.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('google_calendar_id' in test_response.context)                    
                                
#         
#     def test_wikipedia_view(self):
#         '''This tests the google-calendar view.
#         
#         Currently it just ensures that the template is loading correctly.
#         '''
#         test_response = self.client.get('/wikipedia', follow=True)
#         self.assertEqual(test_response.status_code, 200)       
#         self.assertTemplateUsed(test_response, 'wikipedia_edits.html')
#         self.assertTemplateUsed(test_response, 'base.html') 
#         self.assertTemplateUsed(test_response, 'jquery_script.html') 
#         self.assertTrue('pages' in test_response.context)                                 
                                
    def test_news_view(self):
        '''This tests the lab-news view.
        
        Currently it just ensures that the template is loading correctly.
        '''
        test_response = self.client.get('/news', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'lab_news.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        #self.assertTrue('statuses' in test_response.context) 
        self.assertTrue('links' in test_response.context)           
        #self.assertTrue('milestones' in test_response.context) 
        
    def test_contact_page(self):
        '''This tests the contact-page view.
        
        Currently it just ensures that the template is loading correctly.
        '''
        test_response = self.client.get('/contact/', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'contact.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        
    def test_location_page(self):
        '''This tests the location view.
        
        Currently it ensures that the template is loading, and that that the location_list context is passed.
        ''' 
        test_response = self.client.get('/location', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'location.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('lablocation_list' in test_response.context)  
        
class PostModelTests(BasicTests):
    '''This class tests various aspects of the :class:`~papers.models.Post` model.'''
    
    fixtures = ['test_publication','test_publication_personnel', 'test_project', 'test_personnel']   
                
    def test_create_new_post_minimum(self):
        '''This test creates a :class:`~papers.models.Post` with the required information only.'''
        
        test_post = Post(post_title="Test Post",
        author = Person.objects.get(pk=1),
        markdown_url = 'https://raw.githubusercontent.com/BridgesLab/Lab-Website/master/LICENSE.md')
        test_post.save()
        self.assertEqual(test_post.pk, 1) 
        
    def test_create_new_post_all(self):
        '''This test creates a :class:`~papers.models.Post` with all fields entered.'''
        
        test_post = Post(post_title="Test Post",
            author = Person.objects.get(pk=1),
            markdown_url = 'https://raw.githubusercontent.com/BridgesLab/Lab-Website/master/LICENSE.md',
            paper = Publication.objects.get(pk=1),
            project = Project.objects.get(pk=1))
        test_post.save()
        self.assertEqual(test_post.pk, 1) 
        
    def test_post_string(self):
        '''This test creates a :class:`~papers.models.Post` and then verifies the string representation is correct.'''
        
        test_post = Post(post_title="Test Post",
            author = Person.objects.get(pk=1),
            markdown_url = 'https://raw.githubusercontent.com/BridgesLab/Lab-Website/master/LICENSE.md')
        test_post.save()
        self.assertEqual(str(test_post), "Test Post")  
        
    def test_post_slugify(self):
        '''This test creates a :class:`~papers.models.Post` and then verifies the slug representation is correct.'''
        
        test_post = Post(post_title="Test Post",
            author = Person.objects.get(pk=1),
            markdown_url = 'https://raw.githubusercontent.com/BridgesLab/Lab-Website/master/LICENSE.md')
        test_post.save()   
        self.assertEqual(test_post.post_slug, "test-post")   
      
class PostViewTests(BasicTests):
    '''These test the views associated with post objects.'''
    
    fixtures = ['test_post','test_publication','test_publication_personnel', 'test_project', 'test_personnel']   
    
    def test_post_details_view(self):
        """This tests the post-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/fixture-post', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'post_detail.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'disqus_snippet.html')
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')
        self.assertTrue('post' in test_response.context)  
        
        test_response = self.client.get('/posts/not-a-fixture-post', follow=True) 
        self.assertEqual(test_response.status_code, 404)          
        
    def test_post_list(self):
        """This tests the post-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'post_list.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')
        self.assertTrue('post_list' in test_response.context)
        
    def test_post_new(self):
        """This tests the post-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/new', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'post_form.html')
        
    def test_post_edit(self):
        """This tests the post-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/fixture-post/edit', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'post_form.html')
        
        test_response = self.client.get('/posts/not-a-fixture-post/edit', follow=True) 
        self.assertEqual(test_response.status_code, 404)                      
                                                                               
    def test_post_delete(self):
        """This tests the post-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/fixture-post/delete', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertTemplateUsed(test_response, 'base.html')                                                          

        test_response = self.client.get('/posts/not-a-fixture-post/delete', follow=True) 
        self.assertEqual(test_response.status_code, 404)  