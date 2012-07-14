'''This app contains the views for the papers app.

'''
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from papers.models import Publication

class LaboratoryPaperList(ListView):
    '''This class generates the view for laboratory-papers located at **/papers**.
    
    This is filtered based on whether the publication is marked as laboratory_paper = True.
    '''
    queryset = Publication.objects.filter(laboratory_paper=True)
    template_name = "paper-list.html"
    
    def get_context_data(self, **kwargs):
        '''This method adds to the context the paper-list-type  = interesting.'''
        context = super(LaboratoryPaperList, self).get_context_data(**kwargs)
        context['paper-list-type'] = "laboratory"
        return context    
    
class InterestingPaperList(ListView):
    '''This class generates the view for interesting-papers located at **/papers/interesting**.
    
    This is filtered based on whether the publication is marked as interesting_paper = True.
    '''
    queryset = Publication.objects.filter(interesting_paper=True)
    template_name = "paper-list.html"
    
    def get_context_data(self, **kwargs):
        '''This method adds to the context the paper-list-type  = interesting.'''
        context = super(LaboratoryPaperList, self).get_context_data(**kwargs)
        context['paper-list-type'] = "interesting"
        return context       

class PaperDetailView(DetailView):
    '''This class generates the view for paper-details located at **/papers/<title_slug>**.
    
    '''
    model = Publication
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = "paper-detail.html"
    