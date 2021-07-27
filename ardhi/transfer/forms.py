from django import forms
from .models import PropertyTransfer


class TransferForm(forms.ModelForm):
    buyer_email = forms.EmailField(max_length=100, help_text='Buyer email.')

    class Meta:
        model = PropertyTransfer
        fields = ['parcel_no', 'amount', 'file_upload']



# # kill = forms.ModelChoiceField(queryset=Parcels.objects.filter(owner_id=self.owner)
# #         fields = ("kra_pin", "dob", "id_no", "phone", "gender", "profile_image",)
# #         exclude = 'owner'
#
# class SkillForm(ModelForm):
#     skill = forms.ModelChoiceField(queryset= SkillsReference.objects.filter(person = self.person)
#     class Meta:
#         model = Skills
#         fields = ( 'person', 'skill')


# You can ovverride a form structure before you create an instance of the form like:
#
# class SkillForm(ModelForm):
#     class Meta:
#         model = Skills
#
#         fields = ( 'person', 'skill')
# In your view:
#
# SkillForm.base_fields['skill'] = forms.ModelChoiceField(queryset= ...)
# form = SkillForm()


# formset = AuthorFormSet(
#             request.POST, request.FILES,
#             queryset=Author.objects.filter(name__startswith='O'),
#         )
