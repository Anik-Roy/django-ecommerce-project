from django.db import models
# To Create Custom User Model and Admin Panel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy

# To automatically create OneToOne objects
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class MyUserManager(BaseUserManager):
    """ A Custom Manager to deal with emails as unique identifier """
    def _create_user(self, email, password, **extra_fields):
        """ Create and saves a user with a given email and password """
        if not email:
            raise ValueError('The Email must be set!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        ugettext_lazy('staff_status'),
        default=False,
        help_text=ugettext_lazy('Designates weather the user can log in this site')
    )
    is_active = models.BooleanField(
        ugettext_lazy('active'),
        default=True,
        help_text=ugettext_lazy('Designates weather this user should be treated as active. Unselect this insist of deleting account.')
    )
    is_seller = models.BooleanField(
        ugettext_lazy('seller_status'),
        default=False,
        blank=True,
        null=True,
        help_text=ugettext_lazy('Designates weather this user should be treated as a seller. Unselect this insist of a normal account.')
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + '\'profile'

    def is_fully_field(self):
        fields_name = [f.name for f in self._meta.get_fields()]

        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


class SellerInfo(models.Model):
    class ShopType(models.TextChoices):
        electronics = 'electronics', 'Electronics'
        accessories = 'accessories', 'Accessories'
        cloths = 'cloths', 'Cloths'
        groceries = 'groceries', 'Groceries'
        others = 'others', 'Others'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_info')
    shop_name = models.CharField(max_length=264, blank=True)
    shop_address = models.TextField(max_length=350, blank=True)
    shop_type = models.CharField(max_length=50, choices=ShopType.choices, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' seller\'s profile'

    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]

        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

