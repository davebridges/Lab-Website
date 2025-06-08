'''This app contains the views for the :mod`papers` app.

There are three views for this app, :class:`~papers.views.LaboratoryPaperList`, :class:`~papers.views.InterestingPaperList` and :class:`~papers.views.PaperDetailView`

'''
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from papers.models import Publication, Commentary, JournalClubArticle
from papers.context_processors import api_keys
from papers.forms import PublicationForm, PublicationEditForm

class LaboratoryPaperList(ListView):
    '''This class generates the view for laboratory-papers located at **/papers**.
    
    This is filtered based on whether the :class:`~papers.models.Publication` is marked as laboratory_paper = True.
    '''
    queryset = Publication.objects.filter(laboratory_paper=True)
    template_name = "paper-list.html"
    
    def get_context_data(self, **kwargs):
        '''This method adds to the context the paper-list-type  = interesting.'''
        context = super(LaboratoryPaperList, self).get_context_data(**kwargs)
        context['paper_list_type'] = "laboratory"
        return context           
    
class InterestingPaperList(ListView):
    '''This class generates the view for interesting-papers located at **/papers/interesting**.
    
    This is filtered based on whether the :class:`~papers.models.Publication` is marked as interesting_paper = True.
    '''
    queryset = Publication.objects.filter(interesting_paper=True)
    template_name = "paper-list.html"
    
    def get_context_data(self, **kwargs):
        '''This method adds to the context the paper-list-type  = interesting.'''
        context = super(InterestingPaperList, self).get_context_data(**kwargs)
        context['paper_list_type'] = "interesting"
        return context               

class PaperDetailView(DetailView):
    '''This class generates the view for paper-details located at **/papers/<title_slug>**.
    
    '''
    model = Publication
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = "paper-detail.html"
                
class PaperCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~papers.models.Publication`.
    
    It requires the permissions to create a new paper and is found at the url **/paper/new**.'''
    
    permission_required = 'papers.create_publication'
    model = Publication
    form_class = PublicationForm
    template_name = 'publication_form.html'
    
class PaperUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~papers.models.Publication`.
    
    It requires the permissions to update a paper and is found at the url **/paper/<slug>/edit**.'''
    
    permission_required = 'papers.update_publication'
    model = Publication
    form_class = PublicationEditForm
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = 'publication_form.html' 
    
class PaperDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~papers.models.Publication`.
    
    It requires the permissions to delete a paper and is found at the url **/paper/<slug>/delete**.'''
    
    permission_required = 'papers.delete_publication'
    model = Publication
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = 'confirm_delete.html'
    template_object_name = 'object' 
    success_url = reverse_lazy('laboratory-papers')        
                   
    
class CommentaryList(ListView):
    '''This class generates the view for commentaries located at **/papers/commentary**.
    '''
    model = Commentary
    template_name = "commentary-list.html"

    def get_context_data(self, **kwargs):
        context = super(CommentaryList, self).get_context_data(**kwargs)
        context['journal_article_list'] = JournalClubArticle.objects.all()[:10]
        return context
        
class JournalClubList(ListView):
    '''This class generates the view for journal club articles located at **/papers/journal-club**.
    '''
    model = JournalClubArticle
    template_name = "jc-list.html"   
    context_object_name = 'journal_club_list'  

class CommentaryDetail(DetailView):
    '''This class generates the view for commentary-detail located at **/papers/commentary/<pk>**.
    '''
    model = Commentary
    template_name = "commentary-detail.html"
                
class CommentaryCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~papers.models.Commentary`.
    
    It requires the permissions to create a new paper and is found at the url **/papers/commentary/new**.'''
    
    permission_required = 'papers.create_commentary'
    model = Commentary
    fields = "__all__"
    template_name = "commentary-form.html"

class CommentaryUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~papers.models.Commentary`.
    
    It requires the permissions to update a commentary and is found at the url **/paper/commentary/<pk>/edit**.'''
    
    permission_required = 'papers.update_commentary'
    model = Commentary
    fields = "__all__"
    template_name = 'commentary-form.html' 
    
class CommentaryDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~papers.models.Commentary`.
    
    It requires the permissions to delete a paper and is found at the url **/paper/commentary/<pk>/delete**.'''
    
    permission_required = 'papers.delete_commentary'
    model = Commentary
    template_name = 'confirm_delete.html'
    template_object_name = 'object'
    success_url = reverse_lazy('commentary-list') 
