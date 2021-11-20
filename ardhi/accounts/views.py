from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import RegisterForm, LoginForm, AccountUpdateForm, AccountProfileForm
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from parcels.utils import get_ip_address, get_geo
from django.db.models.query_utils import Q
from django.template import RequestContext
from .models import Account, Profile
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views import View
import africastalking
import datetime

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

username = "rundalis"
api_key = "6fd1032dcebdbc0bf7d29d057238ee443ee8388e871aab6da7234f06ff8893bc"
africastalking.initialize(username, api_key)
africastalking.initialize(username, api_key)
sms = africastalking.SMS


# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Account.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # return redirect('login')
            login(request, user)

            messages.success(request, f"Hey {user.username.title()}, Your account have been confirmed..")
            subject = 'Runda LIS Registration.'
            message = f""" Hi {user.first_name} {user.last_name},Thank you for registering to our services. 
            Please find the attached certificate of registration. """

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False, )

            return redirect('home')
        else:
            messages.warning(request, 'The confirmation link was invalid and the token has expired.')
            return redirect('home')


def registration_view(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('accounts/account_activation_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           "token": default_token_generator.make_token(user),
                                       })
            user.email_user(subject, message)

            messages.info(request, 'Please Confirm your email to complete registration.')

            return redirect('login')
        else:
            context['registration_form'] = form

    else:
        form = RegisterForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def profile_view(request, *args, **kwargs):
    log_user = request.user.id
    user_id = get_object_or_404(Account, id=log_user)

    context = {}
    # ip_address = get_ip_address(request)
    # lat, lon = get_geo(ip_address)

    ip = '41.80.98.237'
    lat, lon = get_geo(ip)

    if request.POST:
        form = AccountProfileForm(request.POST, request.FILES)
        if form.is_valid():
            gender = form.cleaned_data.get('gender')
            kra_pin = form.cleaned_data.get('kra_pin')
            id_no = form.cleaned_data.get('id_no')
            dob = form.cleaned_data.get('dob')
            phone = form.cleaned_data.get('phone')
            profile_image = form.cleaned_data.get('profile_image')

            # update user address
            address = Profile(owner_id=user_id.id, gender=gender, kra_pin=kra_pin, id_no=id_no, dob=dob,
                              phone=phone, ip=ip, latitude=lat, longitude=lon, profile_image=profile_image)
            address.save()
            messages.success(request, f"Hey {username}, You Address has been updated..")

            # return redirect('success')
            return redirect("home")
        else:
            context['profile_form'] = form
    else:
        form = AccountProfileForm()
        context['profile_form'] = form
    return render(request, 'accounts/profile.html', context)


def login_view(request):
    context = {}
    new_group, created = Group.objects.get_or_create(name='managers')
    group = Group.objects.get(name='managers')
    model_name = 'manage'
    all_perms_on_this_modal = Permission.objects.filter(codename__contains=model_name)
    group.permissions.set(all_perms_on_this_modal)
    print(all_perms_on_this_modal)
    for permi in all_perms_on_this_modal:
        print(permi)
    from .models import Manager

    # content_type = ContentType.objects.get_for_model(Manager)
    # print(content_type)
    # all_permissions = Permission.objects.filter(content_type=content_type)
    # group.permissions.set(all_permissions)

    # permissions_list = Permission.objects.all()
    # group.permissions.set(all_perms_on_this_modal)

    user = request.user
    if user.is_authenticated:
        messages.success(request, f'Welcome back {request.user}, you have been logged in!')
        return redirect("home")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user.is_active:
                login(request, user)
                messages.success(request, f"{request.user}, Welcome back..")
                return redirect("home")
            else:
                messages.success(request, f"{request.user}, Your account is not activated. Please reactivate")
                return redirect("login")


        else:
            messages.success(request, 'Error while logging in. Please try again')
            return redirect("login")
    else:
        form = LoginForm()
    context['login_form'] = form
    return render(request, "accounts/login.html", context)


def edit_account(request):
    if not request.user.is_authenticated:
        return redirect("login")

    print(all_perms_on_this_modal)
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


def password_reset_request(request):
    if request.method == 'POST':
        pass_form = PasswordResetForm(request.POST)
        if pass_form.is_valid():
            data = pass_form.cleaned_data['email']

            user_mail = Account.objects.filter(Q(email=data))
            if user_mail.exists():
                current_site = get_current_site(request)
                for user in user_mail:
                    subject = "Password Request"
                    email_template_name = "accounts/password_message.txt"
                    parameters = {
                        "email": user.email,
                        "domain": current_site.domain,
                        "user": user,
                        "site_name": 'Ardhi Land Info',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": 'http',
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject, email, '', [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invali Header')
                    return redirect('password_reset_done')
    else:
        pass_form = PasswordResetForm(request.POST)
    context = {
        "pass_form": pass_form,
    }
    return render(request, 'accounts/password_reset_form.html', context)


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

# Create your views here.
# def registration_view(request):
#     user = request.user
#     if user.is_authenticated:
#         return HttpResponse("You are already authenticated as " + str(user.email))
#     context = {}
#     if request.POST:
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             first_name = form.cleaned_data.get('first_name')
#             last_name = form.cleaned_data.get('last_name')
#             email = form.cleaned_data.get('email')
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#
#             # authenticate the user if information is correct and valid
#             account = authenticate(first_name=first_name, last_name=last_name, email=email,
#                                    username=username, password=password)
#
#             messages.success(request, f"Hey {username.title}, You have successfully been Registered..")
#
#             subject = 'Runda LIS Registration.'
#             message = f"""
#             Hi {first_name} {last_name},Thank you for registering to our services.
#             Please find the attached certificate of registration"""
#
#             send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False, )
#
#             if account:
#                 login(request, account)
#
#             messages.success(request, "Hey, You have been registered please update your profile and address")
#             return redirect('home')
#
#         else:
#             context['registration_form'] = form
#
#     else:
#         form = RegisterForm()
#         context['registration_form'] = form
#     return render(request, 'accounts/register.html', context)
