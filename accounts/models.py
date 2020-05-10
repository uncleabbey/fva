from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager 
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class VendorManager(BaseUserManager):
    def create_vendor(self, email, phone_number, business_name, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        vendor = Vendor( email=self.normalize_email(email), phone_number=phone_number, business_name=business_name )
        vendor.set_password(password)
        vendor.save()
        return vendor


class CustomerManager(BaseUserManager):
    def create_customer(self, email, phone_number, first_name, last_name, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        customer = Customer( email=self.normalize_email(email), phone_number=phone_number, first_name=first_name, last_name=last_name )
        customer.set_password(password)
        customer.save()
        return customer

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number',]

    objects = UserManager()

    def __str__(self):
            return self.email



class Vendor(User):
    business_name = models.CharField(_("Business name"), max_length=50)
    dateTimeCreated = models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['phone_number', 'business_name',]

    objects = VendorManager()
    def __str__(self):
            return self.email


class Customer(User):
    amountOutstanding = models.IntegerField(default=0)
    dateTimeCreated = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'amountOutstanding',]


    objects = CustomerManager()

    def __str__(self):
        return self.email

    
