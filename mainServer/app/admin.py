from django.contrib import admin
from .models import CustomUser, Building, VibrationData, Frequency, NumberImage
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
# Register your models here.
class UserCreateForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Retype of Password', 
        widget=forms.PasswordInput,
    )
 
    class Meta:
        model = CustomUser
        fields = ('username', 'date_of_birth')
 
    def check_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        #else if not password1 or not password2:
        #    raise forms.ValidationError("Retype the Password!")
        return password2
 
    def save(self, commit=True):
        user = super().save(commit=False)
        print("save")
        self.check_password()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
 
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'date_of_birth',
                  'is_active', 'is_admin')
 
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
 
    list_display = ('username', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Building)
admin.site.register(VibrationData)
admin.site.register(Frequency)
admin.site.register(NumberImage)
admin.site.unregister(Group)