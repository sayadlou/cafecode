from django.shortcuts import render
from django.core.mail import send_mail


# Create your views here.
def home(request):
    context = {

    }
    return render(request, 'cafecode/home.html', context)



