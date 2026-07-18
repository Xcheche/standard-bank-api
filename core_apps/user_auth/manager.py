import random
import string
from os import getenv
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from typing import Any, Optional
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


# ====================================================
# Generate Username
# ====================================================
def generate_username() -> str:
    bank_name = getenv("BANK_NAME", "bank")
    words = bank_name.split()
    prefix = "".join(word[0].upper() for word in words)
    remaining_length = 12 - len(prefix)
    random_chars = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=remaining_length)
    )
    username = prefix + random_chars
    return username


# ====================================================
# Account Locked Email
# ====================================================


def validate_email_address(email: str) -> None:
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(_("Invalid email address, please provide a valid email."))


# ====================================================
# User Manager
# ====================================================


class UserManager(DjangoUserManager):
    """Custom user manager for handling user creation and management."""

    # Create user method
    def _create_user(self, email: str, password: Optional[str], **extra_fields: Any):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError(_("The Email field must be set"))

        if not password:
            raise ValueError(_("The Password field must be set"))

        validate_email_address(email)

        email = self.normalize_email(email)
        validate_email_address(email)
        username = generate_username()
        user = self.model(email=email, username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    # Create user method
    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> Any:
        """Creates and saves a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    # Create superuser method
    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self._create_user(email, password, **extra_fields)
