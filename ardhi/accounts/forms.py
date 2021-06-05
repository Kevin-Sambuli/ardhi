from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

from .models import Account

# class OwnershipForm(forms.ModelForm):

#     class Meta:
#         model = Account
#         fields = '__all__'


# # multiple files
# class EmailForm(forms.Form):
#     email = forms.EmailField()
#     subject = forms.CharField(max_length=100)
#     attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#     message = forms.CharField(widget=forms.Textarea)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100)  # help_text='Add a valid email address.')

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'username', 'gender', 'kra_pin', 'id_no',
                  'dob', 'phone', 'password1', 'password2',)
        # fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)




# login authenticated users
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login credentials")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username','profile_image')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)
    
    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        # account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account