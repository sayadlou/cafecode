from django.shortcuts import render
from .forms import *
from django.contrib import messages


def contactus(request):
    contact_form = ContactForm()
    if request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.info(request, 'your message has been seved')
            contact_form = ContactForm()
    context = {
        'contact_form': contact_form,
    }
    return render(request, 'contact_us/form.html', context)
