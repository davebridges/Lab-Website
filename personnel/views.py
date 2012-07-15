'''This app contains the views for the personnel app.

'''

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from personnel.models import Personnel

    
class LaboratoryPersonnelList(ListView):
    '''This class generates the view for current laboratory personnel located at **/personnel**.
    
    This is filtered based on whether the ::class:`Personnel` object is marked as current_lab_member = True.
    '''
    queryset = Personnel.objects.filter(current_lab_member=True)
    template_name = "personnel_list.html"
    context_object_name = 'person'
    
    def get_context_data(self, **kwargs):
        '''This method adds to the context the personnel-type  = current.'''
        context = super(LaboratoryPersonnelList, self).get_context_data(**kwargs)
        context['personnel-type'] = "current"
        return context  

class LaboratoryPersonnelDetail(DetailView):
    '''This class generates the view for personnel-details located at **/personnel/<name_slug>**.
    
    '''
    model = Personnel
    slug_field = "name_slug"
    slug_url_kwarg = "name_slug"
    template_name = "personnel_detail.html"  
    context_object_name = 'person'    
