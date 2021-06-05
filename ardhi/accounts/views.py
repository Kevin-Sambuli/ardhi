from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.core.files.storage import default_storage, FileSystemStorage
import os, json, base64, requests
import cv2
from django.core import files
from django.views import View

from django.core.mail import EmailMessage, send_mail
# from .forms import EmailForm, OwnershipForm

from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from .models import Account
import datetime

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

import africastalking

username = "rundalis"
api_key = "6fd1032dcebdbc0bf7d29d057238ee443ee8388e871aab6da7234f06ff8893bc"
africastalking.initialize(username, api_key)
africastalking.initialize(username, api_key)
sms = africastalking.SMS


# class EmailAttachementView(View):
#     form_class = EmailForm
#     template_name = 'ownership/email_attachment.html'

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'email_form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST, request.FILES)

#         if form.is_valid():

#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             email = form.cleaned_data['email']
#             files = request.FILES.getlist('attach')

#             try:
#                 mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
#                 for f in files:
#                     mail.attach(f.name, f.read(), f.content_type)
#                 mail.send()
#                 return render(request, self.template_name,
#                               {'email_form': form, 'error_message': 'Sent email to %s' % email})
#             except:
#                 return render(request, self.template_name,
#                               {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

#         return render(request, self.template_name,
#                       {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})

# Create your views here.
def registration_view(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            gender = form.cleaned_data.get('gender')
            kra_pin = form.cleaned_data.get('kra_pin')
            id_no = form.cleaned_data.get('id_no')
            dob = form.cleaned_data.get('dob')
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password1')

            # authenticate the user if information is correct and valid
            account = authenticate(first_name=first_name, last_name=last_name, email=email,
                                   username=username, gender=gender, kra_pin=kra_pin, id_no=id_no,
                                   dob=dob, phone=phone, password=password)

            login(request, account)

            subject = 'Runda LIS registration.'
            message = f'Hi {first_name} {last_name},Thank you for registering to our services'

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False, )

            # Use the service synchronously
            response = sms.send(message, [phone])
            print(response)

            # return redirect('success')
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, "accounts/login.html", context)


# function for account view
def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST["email"],
                "username": request.POST["username"]
            }
            form.save()
            context["success_message"] = "Account successfully updated"
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['account_form'] = form
    return render(request, "accounts/account.html", context)


def must_authenticate_view(request):
    return render(request, 'accounts/must_authenticate.html', {})


def home_screen_view(request, *args, **kwargs):
    context = {}

    users = Account.objects.all()
    context['users'] = users

    return render(request, "index.html", context)


# view to display all users
def user_list_view(request):
    context = {}
    users = Account.objects.all()
    context['users'] = users

    return render(request, "users_list.html", context)
