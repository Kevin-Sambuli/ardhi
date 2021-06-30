from django import forms
from django.forms import widgets

from .models import PropertySearch


class SearchForm(forms.ModelForm):
    class Meta:
        model = PropertySearch
        fields = ("parcel", "purpose")
        # publish = forms.ModelChoiceField(queryset=Publish.objects.all())
        # authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.fields['parcel'].widget.attrs['class'] = 'form-control'
        self.fields['parcel'].widget.attrs['placeholder'] = 'LR NUmber(LR12872/2)'
        self.fields['parcel'].label = ""

        self.fields['purpose'].widget.attrs['class'] = 'form-control'
        self.fields['purpose'].widget.attrs['placeholder'] = 'purpose'
        self.fields['purpose'].label = ""
