from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from localflavor.generic.models import IBANField


class Account(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    iban_number = IBANField()
    author = models.ForeignKey(User)

    class Meta:
        verbose_name_plural = "accounts"

    def __unicode__(self):
        return self.first_name

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('main:account_edit', kwargs={'pk': self.pk})
