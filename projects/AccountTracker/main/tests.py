from django.test import TestCase

from .models import Account


class AccountModelTest(TestCase):

    def test_string_representation(self):
        account = Account(first_name="Ahmed")
        self.assertEqual(str(account), account.first_name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Account._meta.verbose_name_plural), "accounts")

    def test_get_absolute_url(self):
        account = Account.objects.create(
            first_name="Ahmed", last_name="Etefy",
            iban_number="GB04BARC20474473160944")
        self.assertIsNotNone(account.get_absolute_url())
