from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.
def home(request, tk):
    product = get_object_or_404(Product, url__iexact=tk)
    context = {
        "tk": tk,
        "product": product,
    }
    return render(request, 'product/product.html', context)


def price(request):
    context = {

    }
    return render(request, 'product/price.html', context)
