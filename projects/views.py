'''This app contains the views for the :mod`projects` app.

There are five views for this app:

* :class:`~projects.views.ProjectList`
* :class:`~projects.views.ProjectDetail` 
* :class:`~projects.views.ProjectCreate`
* :class:`~projects.views.ProjectUpdate`
* :class:`~projects.views.ProjectDelete`

'''
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from projects.models import Project
from papers.context_processors import api_keys

class ProjectList(ListView):
    '''This class generates the view for project-list located at **/projects**.
    
    It includes all projects.
    '''
    
    model = Project
    template_name = "project_list.html"               

class ProjectDetailView(DetailView):
    '''This class generates the view for project-details located at **/projects/<title_slug>**.    
    '''
    
    model = Project
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = "project_detail.html"
                
class ProjectCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~projects.models.Project`.
    
    It requires the permissions to create a new project and is found at the url **/projects/new**.
    '''
    
    permission_required = 'projects.create_project'
    model = Project
    template_name = 'project_form.html'
    
class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~projects.models.Project`.
    
    It requires the permissions to update a project and is found at the url **/projects/<slug>/edit**.'''
    
    permission_required = 'projects.update_project'
    model = Project
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = 'project_form.html' 
    
class ProjectDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~projects.models.Project`.
    
    It requires the permissions to delete a paper and is found at the url **/projects/<slug>/delete**.'''
    
    permission_required = 'projects.delete_project'
    model = Project
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = 'confirm_delete.html'
    template_object_name = 'object' 
    success_url = reverse_lazy('project-list')        
