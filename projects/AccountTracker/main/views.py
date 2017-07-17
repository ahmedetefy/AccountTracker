from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404

from .models import Account


class ManipulationPermissionMixin(object):
    """
    Mixin to validate that only the author of
    instance of model:Account is allowed to edit
    or delete it.
    Author: Ahmed Etefy
    """

    def dispatch(self, request, *args, **kwargs):
        obj = super(ManipulationPermissionMixin, self).get_object()
        if not obj.author == self.request.user:
            raise Http404("Permission Denied!")
        return super(
            ManipulationPermissionMixin,
            self).dispatch(request, *args, **kwargs)


class CommonVariablesMixin(object):
    login_url = '/'
    redirect_field_name = ''


class AccountList(CommonVariablesMixin,
                  LoginRequiredMixin,
                  ListView):
    """
    View to display a list of instance of Model:Account
    Author: Ahmed Etefy
    """
    model = Account


class AccountCreate(CommonVariablesMixin,
                    LoginRequiredMixin,
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


class AccountUpdate(CommonVariablesMixin,
                    LoginRequiredMixin,
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


class AccountDelete(CommonVariablesMixin,
                    LoginRequiredMixin,
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
