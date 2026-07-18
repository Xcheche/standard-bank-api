import random
import string


"""Utility functions for user authentication.
This module provides helper functions for generating OTPs and other authentication-related tasks.
"""


def generate_otp(length=6) -> str:
    """Generates a random OTP of specified length."""
    # Generate a random OTP consisting of digits
    return "".join(random.choices(string.digits, k=length))
