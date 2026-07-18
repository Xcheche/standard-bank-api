# forms.py
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    UserChangeForm as DjangoUserChangeForm,
)
from .models import User
from django.core import validators
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User


# ====================================================
# User Creation Form - For creating a new user with custom validation
# ====================================================


class UserCreationForm(DjangoUserCreationForm):
    """Form for creating a new user with custom validation."""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "id_no",
            "security_question",
            "security_answer",
            "is_staff",
            "is_superuser",
        )

    # Override the clean_email method to validate email uniqueness
    def clean_email(self):
        """Validate that the email is unique."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("A user with this email already exists."))
        return email

    # Override the clean_id_no method to validate ID number uniqueness
    def clean_id_no(self):
        """Validate that the ID number is unique."""
        id_no = self.cleaned_data.get("id_no")
        if User.objects.filter(id_no=id_no).exists():
            raise forms.ValidationError(_("A user with this ID number already exists."))
        return id_no

    # Override the clean method to add custom validation for security question and answer
    def clean(self):
        """Custom validation for the form."""
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get("is_superuser")

        security_question = cleaned_data.get("security_question")
        security_answer = cleaned_data.get("security_answer")

        if not is_superuser:
            if not security_question:
                self.add_error(
                    "security_question", _("This field is required for regular users.")
                )
            if not security_answer:
                self.add_error(
                    "security_answer", _("This field is required for regular users.")
                )
        return cleaned_data

    # Override the save method to handle custom logic before saving the user instance
    def save(self, commit=True):
        """This method saves the user instance with custom logic."""
        user = super().save(commit=False)

        # Normalize email to lowercase
        user.email = user.email.lower()

        if commit:
            user.save()
        return user


# ====================================================
# User Change Form - For changing/ updating user details with custom validation
# ====================================================


class UserChangeForm(DjangoUserChangeForm):
    """Form for changing user details with custom validation."""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "id_no",
            "security_question",
            "security_answer",
            "is_active",
            "is_staff",
            "is_superuser",
        )

    # Override the clean_email method to validate email uniqueness, excluding the current user instance
    def clean_email(self):
        """Validate that the email is unique, excluding the current user instance."""
        email = self.cleaned_data.get("email")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_("A user with this email already exists."))
        return email

    # Validate that the ID number is unique, excluding the current user instance
    def clean_id_no(self):
        """Validate that the ID number is unique, excluding the current user instance."""
        id_no = self.cleaned_data.get("id_no")
        if User.objects.exclude(pk=self.instance.pk).filter(id_no=id_no).exists():
            raise forms.ValidationError(_("A user with this ID number already exists."))
        return id_no

    # Override the clean method to add custom validation for security question and answer
    def clean(self):
        """Custom validation for the form."""
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get("is_superuser")
        is_staff = cleaned_data.get("is_staff")
        security_question = cleaned_data.get("security_question")
        security_answer = cleaned_data.get("security_answer")

        if not is_superuser:
            if not security_question:
                self.add_error(
                    "security_question", _("This field is required for regular users.")
                )
            if not security_answer:
                self.add_error(
                    "security_answer", _("This field is required for regular users.")
                )
        return cleaned_data


# TODO: Fix security question and answer validation for superusers and staff users. Currently, the validation logic only checks for regular users, but it should also consider the requirements for superusers and staff users.
# TODO: Create a super user to test the validation logic for superusers and staff users. This will help ensure that the validation rules are correctly applied to all user types.
