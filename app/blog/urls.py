from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='blog'),
    path('<int:tk>/', views.index, name='blog_index'),
    path('post/<str:tk>/', views.detail, name='blog_detail'),
    path('category/<str:cat>', views.category, name='blog_category_cat'),
    path('category/<str:cat>/<int:tk>', views.category, name='blog_category'),

]
