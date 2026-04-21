"""
URL configuration for CursosDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cursos import views as views_cursos

# Importa tus vistas aquí
from inicio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cursos/', views_cursos.registros, name="Principal"), # Le damos la ruta /cursos/
    path('reportes/', include('cursos.urls')),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('servicios/', views.servicios, name='servicios'),
    path('servicios/planificacion-vial/', views.servicio_vial, name='servicio_vial'),
    path('servicios/parques-inteligentes/', views.servicio_parques, name='servicio_parques'),
    path('servicios/redes-iot/', views.servicio_iot, name='servicio_iot'),
    path('servicios/saneamiento-residuos/', views.servicio_residuos, name='servicio_residuos'),
    path('servicios/bosque-vr/', views.servicio_bosque, name='servicio_bosque'),
    path('servicios/soc-ciberseguridad/', views.servicio_soc, name='servicio_soc'),
    path('blog/', views.blog, name='blog'),
    path('blog/parque-verde-gemelo-digital/', views.blog_parque_verde, name='blog_parque_verde'),
    path('blog/movilidad-autonoma/', views.blog_movilidad, name='blog_movilidad'),
    path('blog/escaneo-lidar/', views.blog_lidar, name='blog_lidar'),
    path('blog/sistema-analitico-v21/', views.blog_sav21, name='blog_sav21'),
    path('contacto/', views.contacto, name='contacto'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/movilidad/', views.proyecto_movilidad, name='proyecto_movilidad'),
    path('catalogo/sustentabilidad/', views.proyecto_sustentabilidad, name='proyecto_sustentabilidad'),
    path('catalogo/iot/', views.proyecto_iot, name='proyecto_iot'),
    path('catalogo/lidar/', views.proyecto_lidar, name='proyecto_lidar'),
    path('catalogo/saneamiento/', views.proyecto_saneamiento, name='proyecto_saneamiento'),
    path('catalogo/ciberseguridad/', views.proyecto_ciberseguridad, name='proyecto_ciberseguridad'),
    path('', views.inicio, name='inicio'), # Dejamos la raíz vacía para el inicio
]

# Configuración para ver imágenes en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


