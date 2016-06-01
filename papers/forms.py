'''This package contains forms for the :mod:papers app'''

from django import forms

from papers.models import Publication, AuthorDetails


class PublicationForm(forms.ModelForm):
    '''This class generates the forms for creating and editing publications.

    This form only shows authors which have been pre-ordered but not yet assigned to a publication.

    '''
    authors = forms.ModelMultipleChoiceField(queryset=AuthorDetails.objects.filter(publication__isnull=True),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Publication
        fields = '__all__'
