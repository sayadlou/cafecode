from smtplib import SMTPException

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import *
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .forms import *
from .models import *
from .decorators import *
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from ..cafecode.views import home
from ..site_admin.views import dashboard


class MyPasswordResetView(PasswordResetView):
    template_name = "account/password_reset.html"
    form_class = MyPasswordResetForm


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_sent.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_form.html'
    form_class = MySetPasswordForm


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_done.html'


def random_string():
    return get_random_string(length=32)


def profile(request):
    if not request.user.is_authenticated:
        return redirect(sign_in)
    if not Customer.objects.filter(user=request.user).exists():
        return redirect(sign_in)
    customer = Customer.objects.get(user=request.user)
    context = {
        'customer': customer
    }
    return render(request, 'account/profile.html', context)


def edit_profile(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(sign_in)
        if not Customer.objects.filter(user=request.user).exists():
            return redirect(sign_in)
        customer = Customer.objects.get(user=request.user)
        customer_form = EditCustomerForm(request.POST, request.FILES, instance=customer)
        if customer_form.is_valid():
            customer_form.save()
            messages.info(request, _("Customer profile edited successfully"))
            print("Customer profile edited successfully")
            return redirect(profile)
        else:
            context = {
                'customer_form': customer_form,
            }
            print(request.POST)
            messages.error(request, "Editing field")
            return render(request, 'account/edit_profile.html', context)
    elif request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect(sign_in)
        if not Customer.objects.filter(user=request.user).exists():
            return redirect(sign_in)
        customer = Customer.objects.get(user=request.user)
        customer_form = EditCustomerForm(instance=customer)

        context = {
            'customer_form': customer_form,
        }
        return render(request, 'account/edit_profile.html', context)


def active(request, cat):
    customer = get_object_or_404(Customer, activation_code=cat)
    if not customer.email_confirmed:
        customer.email_confirmed = True
        customer.save()
    context = {
        'customer': customer
    }
    return render(request, 'account/active.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect(profile)
    if request.method == 'POST':
        print(request.POST.get('agree'))
        if not request.POST.get('agree'):
            messages.error(request, "Read agreement")
            return redirect(register)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = Customer.objects.create(user=user)
            form2 = CreateCustomerForm(request.POST, instance=customer)
            if form2.is_valid():
                customer = form2.save()
                user.email = form2.cleaned_data['email']
                my_group = Group.objects.get(name='customer')
                my_group.user_set.add(user)
                user.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                email_content = 'Dear ' + form.cleaned_data['username'] + ' go to' + reverse('active', args=(
                    customer.activation_code,)) + ' to active your account'
                try:
                    send_mail(f"Activation link for {form.cleaned_data['username']}", email_content,
                              'info@cafecode.com',
                              [form2.cleaned_data['email']])
                    return redirect(profile)
                except SMTPException as e:
                    messages.error(request, f"Error in Email sending {e}")
                    user.delete()
                    return redirect(profile)

            else:
                user.delete()
                context = {
                    'signup_form': form,
                    'customer_form': form2,
                }
                return render(request, 'account/register.html', context)
        else:
            context = {
                'signup_form': form,
                'customer_form': CreateCustomerForm(),
            }
            return render(request, 'account/register.html', context)
    else:
        context = {
            'signup_form': CreateUserForm(),
            'customer_form': CreateCustomerForm(),
        }
        return render(request, 'account/register.html', context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username_login')
        password = request.POST.get('password_login')
        remember_me = request.POST.get('rememberMe')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not remember_me:
                request.session.set_expiry(0)
            login(request, user)
            if user.groups.filter(name="customer").exists():
                return redirect(profile)
            elif user.groups.filter(name="admin").exists():
                return redirect(dashboard)
            else:
                messages.error(request, 'your account have a problem contact to admin')
                context = {
                }
                logout(request)
                return render(request, 'account/signin.html', context)
        else:
            messages.error(request, 'Username or password is incorrect')
            context = {
            }
            return render(request, 'account/signin.html', context)
    else:
        context = {
        }
        return render(request, 'account/signin.html', context)


def sign_out(request):
    logout(request)
    return redirect(home)
