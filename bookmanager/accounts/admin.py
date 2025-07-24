from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

UserModel = get_user_model()


@admin.register(UserModel)
class MyUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('username', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Extra info', {'fields': ('bio', 'fav_books')}),
    )

    filter_horizontal = ('fav_books','groups')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'groups'),
        }),
    )


