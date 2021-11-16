from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('<str:tk>/', views.dashboard),
    path('<str:tk>/<str:cat>/', views.dashboard),
    path('<str:tk>/<str:cat>/<str:item>', views.dashboard, name='dashboard'),
]
