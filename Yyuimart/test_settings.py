# test_settings.py

# Import the main settings to use as a base
from Yyuimart.settings import *

# Override specific settings for testing
# Pasword Hasher for making test Fast
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
# Add any other test-specific settings here