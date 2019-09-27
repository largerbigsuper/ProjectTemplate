from django.contrib import admin
from django.contrib.auth import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    parent_fields = {f.name for f in models.User._meta.fields}
    extra_fields = {f.name for f in User._meta.fields} - {f.name for f in models.User._meta.fields}
    extra_fields.remove('create_at')
    extra_fields.remove('update_at')
    
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': tuple(extra_fields)}),
    )


admin.site.register(User, MyUserAdmin)
