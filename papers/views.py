'''This app contains the views for the :mod`papers` app.

There are three views for this app, :class:`~papers.views.LaboratoryPaperList`, :class:`~papers.views.InterestingPaperList` and :class:`~papers.views.PaperDetailView`

'''
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template import RequestContext

from papers.models import Publication
from papers.context_processors import api_keys

class LaboratoryPaperList(ListView):
    '''This class generates the view for laboratory-papers located at **/papers**.
    
    This is filtered based on whether the :class:`~papers.models.Publication` is marked as laboratory_paper = True.
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
    
    This is filtered based on whether the :class:`~papers.models.Publication` is marked as interesting_paper = True.
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
    
    def render_to_response(self, context, **kwargs):
        '''The render_to_response for this view is over-ridden to add the api_keys context processor.'''
        return super(PaperDetailView, self).render_to_response(
                RequestContext(self.request, context, processors=[api_keys]), **kwargs)
    