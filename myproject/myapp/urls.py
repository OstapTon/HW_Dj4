from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('db/', views.total_in_db, name='db'),     # общая сумма из базы данных
    path('view/', views.total_in_view, name='view'),    # через представление
    path('template/', views.total_in_template, name='template'), # через шаблон
    path('about/', views.about, name='about'),
    # path('change_product/<int:product_id>/', views.change_product, name='change_product'),
]