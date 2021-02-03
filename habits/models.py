import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


def generate_global_user_id() -> str:
    # Use random (type 4) UUIDs for a global user ID
    return uuid.uuid4().hex


class User(AbstractBaseUser):
    # the username will be a combination of the email followed by a /
    # followed by the company id, if existent. It is here to satisfy the unique username
    # requirement of Django. Ideally it should be 261 chars, but unique indexed char fields in
    # Postgres can be a max of 255 chars. It is highly unlikely that people will have email
    # addresses in excess of 248 characters which would cause the username to be 255+ chars.
    username = models.CharField(
        max_length=255,
        unique=True,
        help_text=_(
            'Compound username made up of the email address and the company ID.'
            '<br/>Internal use only - user never sees this'
        ),
    )

    # Global user ID, unique
    # Should be used for integrations with external systems wherever possible
    global_id = models.CharField(
        _('Globally unique ID'),
        max_length=100,
        blank=True,
        default=generate_global_user_id,
        unique=True,
        db_index=True,
    )

    email = models.EmailField(
        _('Email'),
    )

    first_name = models.CharField(
        _('first name'), max_length=50, null=True, blank=True, default=None
    )

    last_name = models.CharField(_('last name'), max_length=50, null=True, blank=True, default=None)

    require_password_change = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

