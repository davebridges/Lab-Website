'''This package contains forms for the :mod:papers app'''

from django import forms

from papers.models import Publication, AuthorDetails


class PublicationForm(forms.ModelForm):
    '''This class generates the forms for creating and editing publications.

    '''
    authors = forms.ModelMultipleChoiceField(queryset=AuthorDetails.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Publication
