from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import Http404

from .models import Account
from . import views


class AccountModelTest(TestCase):
    """
    TestCase to run tests on the model:Account
    Author: Ahmed Etefy
    """

    def test_string_representation(self):
        """
        Test that validates the string representation of
        instances of models:Account
        Author: Ahmed Etefy
        """
        account = Account(first_name="Ahmed")
        self.assertEqual(str(account), account.first_name)

    def test_verbose_name_plural(self):
        """
        Test that validates the plural representation of
        instances of models:Account
        Author: Ahmed Etefy
        """
        self.assertEqual(str(Account._meta.verbose_name_plural), "accounts")

    def test_get_absolute_url(self):
        """
        Test that validates the existence of an absolute url
        for each instance of models:Account
        Author: Ahmed Etefy
        """
        user = User.objects.create(username="etefy")
        account = Account.objects.create(
            first_name="Ahmed", last_name="Etefy",
            iban_number="GB04BARC20474473160944", author=user)
        self.assertIsNotNone(account.get_absolute_url())

    def test_unicode_function(self):
        """
        Test that validates the string representation of
        instances of models:Account
        Author: Ahmed Etefy
        """
        account = Account(first_name="Ahmed")
        self.assertEqual(account.__unicode__(), account.first_name)


class HomeViewTest(TestCase):
    """
    TestCase to run tests on the main:HomeView in views.py
    Author: Ahmed Etefy
    """

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class AccountListViewTest(TestCase):
    """
    TestCase that runs tests on both main:AccountList functions
    and its mixins
    Author: Ahmed Etefy
    """

    def setUp(self):
        u = User.objects.create(username="ahmedetefy")
        u.set_password("123the123")
        u.save()
        self.user = u
        user2 = User.objects.create(username="johndoe")
        u.set_password("123the123")
        u.save()
        Account.objects.create(author=u,
                               first_name="Adam",
                               last_name="John",
                               iban_number="GB04BARC20474473160944")
        Account.objects.create(author=user2,
                               first_name="Tom",
                               last_name="Jefferson",
                               iban_number="GB04BARC20474473160944")

    def test_view_list_user_unauthenticated_redirect(self):
        """
        Test for the LoginRequiredMixin in views.py
        Author: Ahmed Etefy
        """
        response = self.client.get(reverse_lazy('main:account_list'))
        self.assertRedirects(response, '/')

    def test_view_list_user_authenticated(self):
        """
        Test to show that main:AccountList view displays all
        saved instance of models:Account
        Author: Ahmed Etefy
        """
        self.client.login(username="ahmedetefy", password="123the123")
        response = self.client.get(reverse_lazy('main:account_list'))
        self.assertContains(response, 'Adam')
        self.assertContains(response, 'Tom')

    def test_one_account_added_to_list(self):
        """
        Test to show thatthat the creation of an instance of models:Account
        reflects in the models:Account listView
        Author: Ahmed Etefy
        """
        self.client.login(username="ahmedetefy", password="123the123")
        Account.objects.create(author=self.user,
                               first_name="Tony",
                               last_name="Nicholson",
                               iban_number="GB04BARC20474473160944")
        response = self.client.get(reverse_lazy('main:account_list'))
        self.assertContains(response, 'Tony')


class AccountCreateViewTest(TestCase):
    """
    TestCase that runs tests on both main:AccountCreate functions
    and its mixins
    Author: Ahmed Etefy
    """

    def setUp(self):
        u = User.objects.create(username="ahmedetefy")
        u.set_password("123the123")
        u.save()

    def test_view_list_unauthenticated_redirect(self):
        """
        Test for the LoginRequiredMixin in views.py
        Author: Ahmed Etefy
        """
        response = self.client.get(reverse_lazy('main:account_list'))
        self.assertRedirects(response, '/')

    def test_create_task_user_authenticated_valid_credentials(self):
        """
        Test for successful Create of an instance of
        models:Account
        Author: Ahmed Etefy
        """
        self.client.login(username="ahmedetefy", password="123the123")
        data = {
            'first_name': u'Tony',
            'last_name': "Nicholson",
            'iban_number': "GB04BARC20474473160944",
        }
        response = self.client.post(reverse_lazy('main:account_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('main:account_list'))

    def test_create_task_user_authenticated_invalid_iban(self):
        """
        Test to validate correct IBAN digits in models:Account.iban_number
        Author: Ahmed Etefy
        """
        self.client.login(username="ahmedetefy", password="123the123")
        data = {
            'first_name': u'Tony',
            'last_name': "Nicholson",
            'iban_number': "GB04BARC20474473160944ee",
        }
        response = self.client.post(reverse_lazy('main:account_new'), data)
        self.assertEqual(response.status_code, 200)

    def test_create_task_user_authenticated_missing_first_name(self):
        """
        Test to validate the required first name field in
        models:Account.first_name
        Author: Ahmed Etefy
        """
        self.client.login(username="ahmedetefy", password="123the123")
        data = {
            'first_name': u'',
            'last_name': "Nicholson",
            'iban_number': "GB04BARC20474473160944",
        }
        response = self.client.post(reverse_lazy('main:account_new'), data)
        self.assertEqual(response.status_code, 200)

    def test_create_task_user_authenticated_last_name(self):
        """
        Test to validate the required last name field in
        models:Account.last_name
        Author: Ahmed Etefy
        """
        self.client.login(username="ahmedetefy", password="123the123")
        data = {
            'first_name': u'Tony',
            'last_name': "",
            'iban_number': "GB04BARC20474473160944",
        }
        response = self.client.post(reverse_lazy('main:account_new'), data)
        self.assertEqual(response.status_code, 200)


class AccountEditViewTest(TestCase):
    """
    TestCase that runs tests on both main:AccountUpdate functions
    and its mixins
    Author: Ahmed Etefy
    """

    def setUp(self):
        u = User.objects.create(username="ahmedetefy")
        u.set_password("123the123")
        u.save()
        self.user = u
        self.request_factory = RequestFactory()
        user2 = User.objects.create(username="johndoe")
        self.account1 = Account.objects.create(author=u,
                                               first_name="Adam",
                                               last_name="John",
                                               iban_number=("GB04BARC" +
                                                            "20474473160944"))
        self.account2 = Account.objects.create(author=user2,
                                               first_name="Tom",
                                               last_name="Jefferson",
                                               iban_number=("GB04BARC" +
                                                            "20474473160944"))

    def test_edit_account_unauthenticated_redirect(self):
        """
        Test for the LoginRequiredMixin in views.py
        Author: Ahmed Etefy
        """
        response = self.client.get(reverse_lazy('main:account_list'))
        self.assertRedirects(response, '/')

    def test_edit_account_with_different_author(self):
        """
        Test for dispatch function in ManipulationPermissionMixin
        in views.py
        Author : Ahmed Etefy
        """
        data = {
            'first_name': u'Tony2',
        }
        request = self.request_factory.post(reverse_lazy(
            'main:account_edit', kwargs={'pk': self.account2.pk}), data)
        request.user = self.user
        with self.assertRaises(Http404):
            views.AccountUpdate.as_view()(
                request, pk=self.account2.pk)

    def test_edit_account_with_authenticated_author(self):
        """
        Test for successful deletion of a particular instance of
        models:Account
        Author: Ahmed Etefy
        """
        data = {
            'first_name': u'Tony2',
            'last_name': "Jack",
            'iban_number': "GB04BARC20474473160944",
        }
        request = self.request_factory.post(reverse_lazy(
            'main:account_edit', kwargs={'pk': self.account1.pk}), data)
        request.user = self.user
        response = views.AccountUpdate.as_view()(request, pk=self.account1.pk)
        self.assertEqual(response.status_code, 302)


class AccountDeleteViewTest(TestCase):
    """
    TestCase that runs tests on both main:AccountDelete functions
    and its mixins
    Author: Ahmed Etefy
    """

    def setUp(self):
        u = User.objects.create(username="ahmedetefy")
        u.set_password("123the123")
        u.save()
        self.user = u
        self.request_factory = RequestFactory()
        user2 = User.objects.create(username="johndoe")
        self.account1 = Account.objects.create(author=u,
                                               first_name="Adam",
                                               last_name="John",
                                               iban_number=("GB04BARC" +
                                                            "20474473160944"))
        self.account2 = Account.objects.create(author=user2,
                                               first_name="Tom",
                                               last_name="Jefferson",
                                               iban_number=("GB04BARC" +
                                                            "20474473160944"))

    def test_delete_account_unauthenticated_redirect(self):
        """
        Test for the LoginRequiredMixin in views.py
        Author: Ahmed Etefy
        """
        response = self.client.get(reverse_lazy('main:account_list'))
        self.assertRedirects(response, '/')

    def test_delete_account_with_different_author(self):
        """
        Test for dispatch function in ManipulationPermissionMixin
        in views.py
        Author : Ahmed Etefy
        """
        request = self.request_factory.post(reverse_lazy(
            'main:account_edit', kwargs={'pk': self.account2.pk}))
        request.user = self.user
        with self.assertRaises(Http404):
            views.AccountDelete.as_view()(
                request, pk=self.account2.pk)

    def test_delete_account_with_authenticated_author(self):
        """
        Test for successful deletion of a particular instance of
        models:Account
        Author: Ahmed Etefy
        """
        request = self.request_factory.post(reverse_lazy(
            'main:account_edit', kwargs={'pk': self.account1.pk}))
        request.user = self.user
        response = views.AccountDelete.as_view()(request, pk=self.account1.pk)
        self.assertEqual(response.status_code, 302)
