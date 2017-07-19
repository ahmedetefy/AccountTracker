from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from localflavor.generic.models import IBANField


@python_2_unicode_compatible
class Account(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    iban_number = IBANField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at.editable = True

    class Meta:
        verbose_name_plural = "accounts"

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('main:account_edit', kwargs={'pk': self.pk})
