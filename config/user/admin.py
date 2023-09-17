from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'avatar',
            'login_tg',
            'chat_id',
        )

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'avatar', 'login_tg', 'chat_id',)
    fieldsets = (
        (None, {'fields': (
            'password', 'email', 'avatar', 'login_tg', 'chat_id',)}),
        ('Права доступа', {'fields': ('is_superuser',
         'is_staff', 'is_active', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'password', 'confirm_password',
                'email', 'avatar', 'login_tg', 'chat_id',)}),
        ('Права доступа', {'fields': ('is_superuser',
         'is_staff', 'is_active', 'user_permissions')}),
    )
    search_fields = ('email', 'login_tg', 'chat_id',)
    ordering = ('id', 'email')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
