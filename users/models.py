# users/models.py
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models

class CustomAccountManager(BaseUserManager):

    def create_user(self, email, full_name, date_of_birth, password):
        user = self.model(email=email, full_name=full_name, date_of_birth=date_of_birth, password=password)
        user.set_password(password)
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, date_of_birth, password):
        user = self.create_user(email=email, full_name=full_name, date_of_birth=date_of_birth, password=password)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # add additional fields in here
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(max_length=9)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['full_name', 'date_of_birth']
    USERNAME_FIELD = 'email'

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email
