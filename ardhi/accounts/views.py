from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, LoginForm, AccountUpdateForm, AccountProfileForm, AccountAddressForm
import africastalking
from .models import Profile, GeoLocation, Address
from .services import get_location

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

username = "rundalis"
api_key = "6fd1032dcebdbc0bf7d29d057238ee443ee8388e871aab6da7234f06ff8893bc"
africastalking.initialize(username, api_key)
africastalking.initialize(username, api_key)
sms = africastalking.SMS


# Create your views here.
def registration_view(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # authenticate the user if information is correct and valid
            account = authenticate(first_name=first_name, last_name=last_name, email=email,
                                   username=username, password=password)
            # login(request, account)

            # data = get_location()
            #
            # location = GeoLocation(owner=request.user.id, ip=data["ip"],
            #                        country_name=data["country_name"], region_code=data["region_code"],
            #                        city=data["city"], latitude=data['latitude'],
            #                        longitude=data['longitude'], zip_code=data['zip'],).
            # location.save()

            messages.success(request, f"Hey {username}, You have successfully been Registered..")

            subject = 'Runda LIS Registration.'
            message = f"""
            Hi {first_name} {last_name},Thank you for registering to our services. 
            Please find the attached certificate of registration"""

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False, )

            return redirect('login')
        else:
            context['registration_form'] = form

    else:
        form = RegisterForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def profile_view(request):
    context = {}
    if request.POST:
        form = AccountProfileForm(request.POST)
        if form.is_valid():
            form.save()

            gender = form.cleaned_data.get('gender')
            kra_pin = form.cleaned_data.get('kra_pin')
            id_no = form.cleaned_data.get('id_no')
            dob = form.cleaned_data.get('dob')
            phone = form.cleaned_data.get('phone')

            # update user profile
            profile = Profile(owner_id=request.user.id, gender=gender, kra_pin=kra_pin, id_no=id_no,
                              dob=dob, phone=phone)
            profile.save()

            messages.success(request, f"Hey {username}, You have successfully Updated your profile..")

            # return redirect('success')
            return redirect('home')
        else:
            context['profile_form'] = form
    else:
        form = AccountProfileForm()
        context['profile_form'] = form
    return render(request, 'accounts/profile.html', context)


def address_view(request):
    context = {}
    if request.POST:
        form = AccountAddressForm(request.POST)
        if form.is_valid():
            form.save()
            street = form.cleaned_data.get('street')
            city = form.cleaned_data.get('city')
            code = form.cleaned_data.get('code')

            # update user address
            address = Address(owner_id=request.user.id, street=street, city=city, code=code)
            address.save()

            # return redirect('success')
            return redirect('home')
        else:
            context['address_form'] = form
    else:
        form = AccountAddressForm()
        context['address_form'] = form
    return render(request, 'accounts/address.html', context)


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        messages.success(request, f'Welcome back {request.user.username}, you have been logged in!')
        return redirect("home")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            return redirect('home')

            # data = get_location()
            #
            # location = GeoLocation(owner=request.user.id, ip=data["ip"],
            #                        country_name=data["country_name"], region_code=data["region_code"],
            #                        city=data["city"], latitude=data['latitude'],
            #                        longitude=data['longitude'], zip_code=data['zip'],)
            # location.save()

        else:
            messages.success(request, 'Error while logging in. Please try again')
            return redirect('login')
    else:
        form = LoginForm()
    context['login_form'] = form
    return render(request, "accounts/login.html", context)


def edit_account(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST["email"],
                "username": request.POST["username"],
            }
            form.save()
            context["success_message"] = "Account successfully updated"
            messages.success(request, f" Hey ,{request.user.username}, You have edited your profile")
            return redirect('home')
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['account_form'] = form
    return render(request, "accounts/edit_account.html", context)


def update_password(request):
    context = {}
    if request.POST:
        form = PasswordChangeForm(data=request.POST, instance=request.user.id)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'You have edited your Password')
            return redirect('home')
        else:
            messages.success(request, 'Error while changing your password. Please try again')
            return redirect('login')
    else:
        form = PasswordChangeForm(user=request.user)
    context['password_form'] = form
    return render(request, "accounts/update_password.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, f'You {request.user.username} have been logged out!')

    return redirect('home')
