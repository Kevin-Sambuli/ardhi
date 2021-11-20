from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from django.db.models import Q
import geocoder

from django.db import models
from .managers import UserManager, LandownerManager, AgentManager, SurveyorManager, ManagerManager


class Account(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        LANDOWNER = "landowner", "LANDOWNER"
        AGENT = "agent", "AGENT"
        SURVEYOR = "surveyor", "SURVEYOR"
        MANAGER = "manager", "MANAGER"

    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    email = models.EmailField(verbose_name='Email', blank=False, max_length=100, unique=True)
    username = models.CharField('Username', max_length=30, unique=True)
    type = models.CharField(_('Type'), max_length=30, choices=Types.choices, default=Types.LANDOWNER)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    # types = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True)

    # permissions
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField('admin', default=False)
    is_active = models.BooleanField('active', default=False)
    is_staff = models.BooleanField('staff', default=False)
    is_superuser = models.BooleanField('superuser', default=False)

    # unique parameter that will be used to login in the user
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    # hooking the New customized Manager to our Model
    objects = UserManager()

    class Meta:
        db_table = 'accounts'
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return '{}'.format(self.get_full_name())

    def get_full_name(self):
        """ Returns the first_name plus the last_name, with a space in between. """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message):
        """Sends an email to this User. """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email], fail_silently=False)


# class CustomerAdditional(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     address = models.CharField(max_length=1000)
#
#
# class SellerAdditional(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     gst = models.CharField(max_length=10)
#     warehouse_location = models.CharField(max_length=1000)


# # Proxy Models. They do not create a seperate table
class Landowner(Account):
    default_type = Account.Types.LANDOWNER
    objects = LandownerManager()

    class Meta:
        proxy = True
        permissions = (
            ('can_manage_account', 'can manage account'),
        )

    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional


class Agent(Account):
    default_type = Account.Types.AGENT
    objects = AgentManager()

    class Meta:
        proxy = True
        permissions = (
            ('agent_landowners', 'can agent landowners'),
            ('agent_surveyors', 'can agent surveyors'),
        )

    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional


class Surveyor(Account):
    default_type = Account.Types.SURVEYOR

    objects = SurveyorManager()

    class Meta:
        proxy = True
        permissions = (
            ('can_process_survey', 'can process survey'),
        )

    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional


class Manager(Account):
    default_type = Account.Types.MANAGER
    objects = ManagerManager()

    class Meta:
        proxy = True
        permissions = (
            ('can_manage_landowners', 'can manage landowners'),
            ('can_manage_agents', 'can manage agents'),
            ('can_manage_surveyors', 'can manage surveyors'),
        )

    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional


def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'


def get_default_profile_image():
    return "profile_images/profile_image.png"


class Profile(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=True,
                                 null=True, default=None)
    gender = models.CharField('Gender', max_length=5, choices=GENDER)
    kra_pin = models.CharField('KRA PIN', max_length=20, unique=True, null=True, blank=False)
    id_no = models.CharField('ID NO', max_length=10, unique=True, blank=False, null=True, )
    dob = models.DateField('Date of Birth', blank=False, null=True)
    phone = models.CharField('Contact Phone', max_length=10, null=True, blank=True, unique=True)
    profile_image = models.ImageField("Profile Image", max_length=255, upload_to='profile_images', null=True,
                                      blank=True, default=get_default_profile_image)
    ip = models.CharField("Ip Address", max_length=20, null=True, blank=True, )
    latitude = models.DecimalField("Latitude", max_digits=10, decimal_places=6, null=True, blank=True, )
    longitude = models.DecimalField("Longitude", max_digits=10, decimal_places=6, null=True, blank=True, )

    class Meta:
        db_table = 'profile'
        verbose_name = "Profile"
        verbose_name_plural = "User Profile"

    def __str__(self):
        return '{}'.format(self.ip)

    def baby_boomer_status(self):
        """Returns the person's baby-boomer status."""
        import datetime
        if self.dob < datetime.date(1930, 1, 1):
            return "your age is invalid enter the correct birth date"
        elif (datetime.date.today() - self.dob).days // 365 <= 18:
            return "You are not legible to own a land"
        else:
            return "Post-boomer"

    # elif dob < datetime.date(1920, 1, 1):
    #     print("your age is invalid enter the correct birth date")
    # elif (datetime.date.today() - dob).days // 365 <= 18:
    #     print("You are not legible to own a land")
    # elif (dob - datetime.date.today()).days // 365 <= 0:
    #     print("You are not legible to own a land")
    # else:

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]
