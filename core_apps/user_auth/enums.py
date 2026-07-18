from django.db import models  # noqa
from django.utils.translation import gettext_lazy as _

# ====================================================
# Security Questions
# ====================================================


class SecurityQuestions(models.TextChoices):
    MOTHERS_MAIDEN_NAME = "MOTHERS_MAIDEN_NAME", _("What is your mother's maiden name?")
    FIRST_PET = "FIRST_PET", _("What was the name of your first pet?")
    FAVORITE_TEACHER = "FAVORITE_TEACHER", _("Who was your favorite teacher?")
    BIRTH_CITY = "BIRTH_CITY", _("In which city were you born?")
    FAVORITE_FOOD = "FAVORITE_FOOD", _("What is your favorite food?")
    CHILDHOOD_FRIEND = "CHILDHOOD_FRIEND", _(
        "What is the name of your childhood best friend?"
    )
    FIRST_CAR = "FIRST_CAR", _("What was the make and model of your first car?")
    FAVORITE_COLOR = "FAVORITE_COLOR", _("What is your favorite color?")
    HIGH_SCHOOL = "HIGH_SCHOOL", _("What is the name of your high school?")
    FAVORITE_SPORT = "FAVORITE_SPORT", _("What is your favorite sport?")


class AccountStatus(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    LOCKED = "LOCKED", _("Locked")
    SUSPENDED = "SUSPENDED", _("Suspended")


class RoleChoices(models.TextChoices):
    CUSTOMER = "CUSTOMER", _("Customer")
    ACCOUNT_EXECUTIVE = "ACCOUNT_EXECUTIVE", _("Account Executive")
    TELLER = "TELLER", _("Teller")
    BRANCH_MANAGER = "BRANCH_MANAGER", _("Branch Manager")
