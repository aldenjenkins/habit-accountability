from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class TimeStampedModel(models.Model):
    """
    This is a copy of the  django_extensions.db.models.TimeStampedModel
    which uses different names for the created and modified fields in the DB.
    This is done so that we do not have to re-do the existing model migrations
    which originally had the update_ts and create_ts fields.

    TimeStampedModel
    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """

    create_ts = CreationDateTimeField(_('Created'))
    update_ts = ModificationDateTimeField(_('Modified'))

    class Meta:
        get_latest_by = 'update_ts'
        ordering = (
            '-update_ts',
            '-create_ts',
        )
        abstract = True
