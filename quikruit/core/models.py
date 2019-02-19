from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from quikruit.mixins import StringBasedModelIDMixin
from applicants import models as applicant_models

class QuikruitAccountManager(BaseUserManager):
    def _create_user(self, email, password=None, **kwargs):

        if not email:
            raise ValueError("Email must be present for _create_user()")
        new_user = QuikruitAccount(email=self.normalize_email(email), **kwargs)
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_user(self, email, password=None, **kwargs):
        return self._create_user(email, password, is_superuser=False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, is_superuser=True,
            is_staff=True, is_active=True, **kwargs)

# Custom user model
class QuikruitAccount(StringBasedModelIDMixin, AbstractBaseUser):

    email = models.EmailField(unique=True)

    is_active = models.BooleanField(
        "active account", 
        default=False
    )

    is_staff = models.BooleanField(
        "can access admin site", 
        default=False
    )

    is_superuser = models.BooleanField(
        "superuser privileges", 
        default=False
    )
    
    date_created = models.DateField(
        "date of account creation", 
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Quikruit account"
        verbose_name_plural = "Quikruit accounts"

    objects = QuikruitAccountManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_module_perms(self, package_name):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    @property
    def is_applicant(self):
        try:
            profile = self.applicant_profile
            return True
        except ApplicantProfile.DoesNotExist:
            return False