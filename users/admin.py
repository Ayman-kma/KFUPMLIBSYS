from django.contrib import admin

# Register your models here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

class UserCreationFormExtended(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super(UserCreationFormExtended, self).__init__(*args, **kwargs) 

UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'email', 'first_name', 'last_name' ,'password1', 'password2',)
    }),
)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)