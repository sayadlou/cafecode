from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('cafecode/<str:tk>/', views.home, name='product'),
    path('order/', TemplateView.as_view(template_name="product/order.html"), name='order'),
    path('price/', views.price, name='price'),

]
