from django.contrib.auth.models import BaseUserManager
from django.db.models import Q
from django.db import models
from django.conf import settings


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
        # user.Types.MANAGER
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Model Managers for proxy models
class LandownerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.SELLER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains=settings.AUTH_USER_MODEL.Types.LANDOWNER))


class AgentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.CUSTOMER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains=settings.AUTH_USER_MODEL.Types.AGENT))


class SurveyorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.SELLER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains=settings.AUTH_USER_MODEL.Types.SURVEYOR))


class ManagerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.CUSTOMER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains=settings.AUTH_USER_MODEL.Types.MANAGER))
