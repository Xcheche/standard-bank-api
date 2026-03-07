import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone

from core_apps.user_auth.enums import SecurityQuestions
from .manager import UserManager
from django.utils.translation import gettext_lazy as _
from .emails import send_account_locked_email
from .enums import SecurityQuestions, AccountStatus, RoleChoices

# Create your models here.

# Custom User model
class User(AbstractUser):
  
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=12, unique=True)
    security_question = models.CharField(max_length=30, 
                                         verbose_name=_('Security Question'),
                                         choices=SecurityQuestions.choices) 
    security_answer = models.CharField(_('Security Answer'), max_length=255)
    email = models.EmailField(_('Email Address'), unique=True,db_index=True) 
    first_name = models.CharField(_('First Name'), max_length=30)
    middle_name = models.CharField(_('Middle Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30)
    id_no =models.PositiveIntegerField(_('ID Number'), unique=True)
    account_status = models.CharField(_('Account Status'),
                                          max_length=10,
                                          choices=AccountStatus.choices,
                                          default=AccountStatus.ACTIVE)
    role = models.CharField(_('Role'),
                            max_length=20,
                            choices=RoleChoices.choices,
                            default=RoleChoices.CUSTOMER)
    failed_login_attemps =  models.PositiveSmallIntegerField(_('Failed Login Attempts'), default=0)
    last_failed_login = models.DateTimeField(_('Last Failed Login'), null=True, blank=True)
    otp = models.CharField(_('OTP'), max_length=6, blank=True )
    otp_expiry_time = models.DateTimeField(_("OTP Expiry Time"), null=True, blank=True)
    #Model manager
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "id_no",
        "security_question",
        "security_answer",
    ]

    # Override save method to handle account locking and unlocking
    def set_otp(self,otp:str)->None:
        self.otp = otp
        self.otp_expiry_time = timezone.now() + settings.OTP_EXPIRATION_TIME
        self.save()

    # Override save method to handle account locking and unlocking
    def verify_otp(self, otp:str)->bool:
        if self.otp == otp and self.otp_expiry_time > timezone.now():
            self.otp = ""
            self.otp_expiry_time = None
            self.save()
            return True
        return False    