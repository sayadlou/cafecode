from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.utils.translation import ugettext_lazy as _

title = (
    ("Herr", _("Mr")),
    ("Frau", _("Mrs")),
)


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        }),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        }),
    )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=50)
    email.widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
    email.error_messages = {
        'required': _('Enter your Email'),
        'max_length': _('email is too long'),
    }


class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'email_confirmed', 'activation_code', 'password_reset_code']

    title = forms.ChoiceField(label='Anrede', required=False, choices=title)
    name = forms.CharField(label='Vorname', required=False, max_length=50)
    email = forms.EmailField(max_length=50)

    title.widget.attrs.update({'class': 'form-control', 'placeholder': _('Title')})
    name.widget.attrs.update({'class': 'form-control', 'placeholder': _('First and Last Name')})
    email.widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
    title.error_messages = {
        'required': _('Enter your title'),
        'max_length': _('title is too long'),
    }
    name.error_messages = {
        'required': _('Enter your name'),
        'max_length': _('name is too long'),
    }

    email.error_messages = {
        'required': _('Enter your Email'),
        'max_length': _('email is too long'),
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Email already exists"))
        return email


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('User name'),
    }),
        label='username'
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': _('Password'),
    }),
        label=_('Password')
    )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': _('Repeat password'),
    }),
        label=_('Repeat password')
    )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password', ]

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('User name'),
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': _('Password'),
    }))



class EditCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'email_confirmed', 'activation_code', 'password_reset_code']

    title = forms.ChoiceField(label='Anrede', required=False, choices=title)
    name = forms.CharField(label='Vorname', required=False, max_length=50)
    company_name = forms.CharField(label=_("Company name"), required=False, max_length=50)
    address = forms.CharField(widget=forms.Textarea, label=_("Address"), required=False, max_length=50)
    phone_number = forms.CharField(label=_("Phone number"), required=False, max_length=15)
    picture = forms.ImageField()

    title.widget.attrs.update({'class': 'form-control', 'placeholder': _('Title')})
    name.widget.attrs.update({'class': 'form-control', 'placeholder': _('First and Last Name')})
    company_name.widget.attrs.update({'class': 'form-control', 'placeholder': _('Company name')})
    address.widget.attrs.update({'class': 'form-control', 'placeholder': _('Address'), 'rows': '5'})
    phone_number.widget.attrs.update({'class': 'form-control', 'placeholder': _('Phone number')})
    picture.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    picture.widget.template_name = 'input/clearable_file_input.html'
    title.error_messages = {
        'required': _('Enter your title'),
        'max_length': _('title is too long'),
    }
    name.error_messages = {
        'required': _('Enter your name'),
        'max_length': _('name is too long'),
    }
    picture.error_messages = {
        'required': _('Please send a picture'),
        'max_length': _('name is too long'),
    }


# class EditUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password1', 'password2']
#
#     username = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': _('User name'),
#     }),
#         label='username'
#     )
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'placeholder': _('Password'),
#     }),
#         label=_('Password')
#     )
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'placeholder': _('Repeat password'),
#     }),
#         label=_('Repeat password')
#     )
