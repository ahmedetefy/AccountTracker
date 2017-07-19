from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
import datetime

from .models import Account


class ManipulationPermissionMixin(object):
    """
    Mixin to validate that only the author of
    instance of model:Account is allowed to edit
    or delete it.
    Author: Ahmed Etefy
    """

    def get_object(self, queryset=None):
        """
        Returns an instance of model:Account in the case that
        the author of the instance of model:Account is the
        the user logged in
        otherwise it raises a HTTP404 Error
        Author: Ahmed Etefy
        """
        obj = super(ManipulationPermissionMixin, self).get_object()
        if not obj.author == self.request.user:
            raise Http404("Permission Denied!")
        return obj


class AccountList(LoginRequiredMixin,
                  ListView):
    """
    View to display a list of instance of Model:Account
    Author: Ahmed Etefy
    """
    model = Account


class AccountCreate(LoginRequiredMixin,
                    CreateView):
    """
    View to create an instance of Model:Account with fields
    Account.first_name, Account.last_name, Account.iban_number.
    Author: Ahmed Etefy
    """
    model = Account
    fields = ['first_name', 'last_name', 'iban_number']
    success_url = reverse_lazy('main:account_list')

    def form_valid(self, form):
        """
        Function to set author of the Model:Account instance to
        be created as the currently authenticated User.
        """
        form.instance.author = self.request.user
        return super(AccountCreate, self).form_valid(form)


class AccountUpdate(LoginRequiredMixin,
                    ManipulationPermissionMixin,
                    UpdateView):
    """
    View to allow author of instance of Model:Account to update
    his instance of Model:Account with fields
    Account.first_name, Account.last_name, Account.iban_number.
    Author: Ahmed Etefy
    """
    model = Account
    fields = ['first_name', 'last_name', 'iban_number']
    success_url = reverse_lazy('main:account_list')

    def get_object(self, queryset=None):
        """
        Returns an instance of model:Account in the case that
        less than two hours from creation time had elapsed
        otherwise it raises a HTTP404 Error
        Author: Ahmed Etefy
        """
        obj = super(AccountUpdate, self).get_object()
        currentTime = datetime.datetime.now()
        creationTime = obj.created_at.replace(tzinfo=None)
        secDifference = (currentTime - creationTime).total_seconds()
        hourDifference = secDifference / 3600
        if hourDifference > 2:
            raise Http404("You can no longer edit this entry!")
        return obj


class AccountDelete(LoginRequiredMixin,
                    ManipulationPermissionMixin,
                    DeleteView):
    """
    View to allow author of instance of Model:Account to update
    his instance of Model:Account with fields
    Account.first_name, Account.last_name, Account.iban_number.
    Author: Ahmed Etefy
    """
    model = Account
    success_url = reverse_lazy('main:account_list')


class HomeView(TemplateView):
    """
    A home page view for the application
    Author: Ahmed Etefy
    """
    template_name = 'main/index.html'
