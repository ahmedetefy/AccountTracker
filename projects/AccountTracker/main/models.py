from django.db import models
from django.core.urlresolvers import reverse
from localflavor.generic.models import IBANField


class Account(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    iban_number = IBANField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:account_edit', kwargs={'pk': self.pk})
