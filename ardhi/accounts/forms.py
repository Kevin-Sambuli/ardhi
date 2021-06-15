from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms
from .models import Account, Profile, Address


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label="", max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Email address'}))

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ""

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ""

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ""

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


class AccountProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("kra_pin", "dob", "id_no", "phone", "gender", "profile_image",)

    def __init__(self, *args, **kwargs):
        super(AccountProfileForm, self).__init__(*args, **kwargs)

        self.fields['kra_pin'].widget.attrs['class'] = 'form-control'
        self.fields['kra_pin'].widget.attrs['placeholder'] = 'KRA PIN'
        self.fields['kra_pin'].label = ""

        self.fields['id_no'].widget.attrs['class'] = 'form-control'
        self.fields['id_no'].widget.attrs['placeholder'] = 'Id Number'
        self.fields['id_no'].label = ""

        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['placeholder'] = 'Telephone'
        self.fields['phone'].label = ""

        self.fields['dob'].widget.attrs['class'] = 'form-control'
        self.fields['dob'].widget.attrs['placeholder'] = 'Date of Birth'
        self.fields['dob'].label = ""


class AccountAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("street", "city", "code")

    def __init__(self, *args, **kwargs):
        super(AccountAddressForm, self).__init__(*args, **kwargs)

        self.fields['street'].widget.attrs['class'] = 'form-control'
        self.fields['street'].widget.attrs['placeholder'] = 'Street'
        self.fields['street'].label = ""

        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['city'].label = ""

        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['code'].widget.attrs['placeholder'] = 'Code'
        self.fields['code'].label = ""


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter valid email'
        self.fields['email'].label = ""

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'password'
        self.fields['password'].label = ""

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login credentials")


class AccountUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))

    class Meta:
        model = Account
        fields = ('email', 'username')

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
        if commit:
            account.save()
        return account
