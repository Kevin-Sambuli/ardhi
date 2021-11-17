from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from django.db import models
import geocoder


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('Please provide a valid email')
        if not username:
            raise ValueError('Please provide a username')
        if not first_name:
            raise ValueError('Provide your first Name')
        if not last_name:
            raise ValueError('Provide your last Name')

        user = self.model(
            email=self.normalize_email(email), username=username, first_name=first_name,
            last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    email = models.EmailField(verbose_name='Email', blank=False, max_length=100, unique=True)
    username = models.CharField('Username', max_length=30, unique=True)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)

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
        # full_name= str(full_name.title)
        return full_name.strip()

    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message):
        """Sends an email to this User. """
        # message = f"""Hi {self.first_name}{self.last_name}, You have successfully been Registered to Ardhi Land
        #           Information System. Please find the attached certificate of registration. """
        # subject = "Ardhi LIS Registration"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email], fail_silently=False)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


# @receiver(post_save, sender=Account)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Account.objects.create(user=instance)


# @receiver(post_save, sender=Account)
# def save_user_profile(sender, instance, **kwargs):
#     instance.account.save()


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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=True,
                              null=True, default=None)
    gender = models.CharField('Gender', max_length=5, choices=GENDER)
    kra_pin = models.CharField('KRA PIN', max_length=20, unique=True, null=True, blank=False)
    id_no = models.CharField('ID NO', max_length=10, unique=True, blank=False, null=True,)
    dob = models.DateField('Date of Birth', blank=False, null=True)
    phone = models.CharField('Contact Phone', max_length=10, null=True, blank=True, unique=True)
    profile_image = models.ImageField("Profile Image", max_length=255, upload_to='profile_images', null=True,
                                      blank=True, default=get_default_profile_image)
    ip = models.CharField("Ip Address", max_length=20, null=True, blank=True, )
    latitude = models.DecimalField("Latitude", max_digits=10, decimal_places=6, null=True, blank=True, )
    longitude = models.DecimalField("Longitude", max_digits=10, decimal_places=6, null=True, blank=True,)

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
