from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^list$', views.AccountList.as_view(), name='account_list'),
    url(r'^new$', views.AccountCreate.as_view(), name='account_new'),
    url(r'^edit/(?P<pk>\d+)$',
        views.AccountUpdate.as_view(), name='account_edit'),
    url(r'^delete/(?P<pk>\d+)$',
        views.AccountDelete.as_view(), name='account_delete'),
]
