from django.contrib import admin

from .models import Account

# Register your models here.


# class AccountAdmin(admin.ModelAdmin):
#     def has_change_permission(self, request, obj=None):
#         return obj is None or obj.author == request.user

#     def has_delete_permission(self, request, obj=None):
#         return obj is None or obj.author == request.user

admin.site.register(Account)