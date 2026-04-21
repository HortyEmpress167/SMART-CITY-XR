from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.lista_problemas, name='lista_problemas'),
    path('nuevo/', views.reportar_problema, name='reportar_problema'),
    path('votar/<int:problema_id>/', views.votar_problema, name='votar_problema'),
    path('cotizar/', views.solicitar_cotizacion, name='solicitar_cotizacion'),
]
