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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=12, unique=True)
    security_question = models.CharField(
        max_length=30,
        verbose_name=_("Security Question"),
        choices=SecurityQuestions.choices,
    )
    security_answer = models.CharField(_("Security Answer"), max_length=255)
    email = models.EmailField(_("Email Address"), unique=True, db_index=True)
    first_name = models.CharField(_("First Name"), max_length=30)
    middle_name = models.CharField(_("Middle Name"), max_length=30, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=30)
    id_no = models.PositiveIntegerField(_("ID Number"), unique=True)
    account_status = models.CharField(
        _("Account Status"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )
    role = models.CharField(
        _("Role"),
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER,
    )
    failed_login_attempts = models.PositiveSmallIntegerField(
        _("Failed Login Attempts"), default=0
    )
    last_failed_login = models.DateTimeField(
        _("Last Failed Login"), null=True, blank=True
    )
    otp = models.CharField(_("OTP"), max_length=6, blank=True)
    otp_expiry_time = models.DateTimeField(_("OTP Expiry Time"), null=True, blank=True)
    # Model manager
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
    def set_otp(self, otp: str) -> None:
        self.otp = otp
        self.otp_expiry_time = timezone.now() + settings.OTP_EXPIRATION_TIME
        self.save()

    # Override save method to handle account locking and unlocking
    def verify_otp(self, otp: str) -> bool:
        if self.otp == otp and self.otp_expiry_time > timezone.now():
            self.otp = ""
            self.otp_expiry_time = None
            self.save()
            return True
        return False

    # Protection against brute-force attacks: Locks account after a certain number of failed attemps
    def handle_failed_login_attempt(self):

        self.failed_login_attemps += 1
        self.last_failed_login = timezone.now()
        if self.failed_login_attemps >= settings.LOGIN_ATTEMPT:
            self.account_status = AccountStatus.LOCKED
            send_account_locked_email(self.email)
        self.save()

    # Reset failed login attempts after a successful login
    def reset_failed_login_attempts(self) -> None:
        self.failed_login_attemps = 0
        self.last_failed_login = None
        self.account_status = AccountStatus.ACTIVE
        self.save()

    # Unlocks the account after a certain duration
    def unlock_account(self) -> None:
        if self.account_status == AccountStatus.LOCKED:
            self.account_status = AccountStatus.ACTIVE
            self.failed_login_attemps = 0
            self.last_failed_login = None
            self.save()

    # Property to check if the account is locked
    @property
    def is_account_locked(self) -> bool:
        if self.account_status == AccountStatus.LOCKED:
            if (
                self.last_failed_login
                and timezone.now() - self.last_failed_login >= settings.LOGOUT_DURATION
            ):
                self.unlock_account()
                return False
            return True
        return False

    # Property to get the full name of the user
    @property
    def full_name(self) -> str:
        full_name = f"{self.first_name} {self.last_name}".strip()
        return " ".join(
            full_name.split()
        )  # Remove extra spaces if middle name is empty

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    # Custom method to check if the user has a specific role
    def has_role(self, role_name: str) -> bool:
        return hasattr(self, "role") and self.role == role_name

    def __str__(self) -> str:
        return f"{self.full_name} -{self.get_role_display()} ({self.email})"
