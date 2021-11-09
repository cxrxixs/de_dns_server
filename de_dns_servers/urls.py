from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.filter_de_dns_server, name='filter_de_dns_server'),
    path('api/dns', views.api_de_dns_server, name='api_de_dns_server'),
]