from django import forms
from .models import PropertySearch


class SearchForm(forms.ModelForm):
    class Meta:
        model = PropertySearch
        # fields = ("parcel", "purpose")
        fields = ("owner", "parcel", "purpose")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)


        # self.fields['owner'].widget.attrs['class'] = 'hidden'

        self.fields['parcel'].widget.attrs['class'] = 'form-control'
        self.fields['parcel'].widget.attrs['placeholder'] = 'LR NUmber(LR12872/2)'
        self.fields['parcel'].label = ""

        self.fields['purpose'].widget.attrs['class'] = 'form-control'
        self.fields['purpose'].widget.attrs['placeholder'] = 'purpose'
        self.fields['purpose'].label = ""
