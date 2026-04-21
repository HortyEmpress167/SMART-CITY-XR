# en inicio/views.py
from django.shortcuts import render
from cursos.models import Servicio

def inicio(request):
    servicios = Servicio.objects.all()
    return render(request, 'cursos/cursos.html', {'servicios': servicios})

def nosotros(request):
    return render(request, 'inicio/nosotros.html')

def servicios(request):
    return render(request, 'inicio/servicios.html')

def servicio_vial(request):
    return render(request, 'inicio/servicio_vial.html')
    
def servicio_parques(request):
    return render(request, 'inicio/servicio_parques.html')
    
def servicio_iot(request):
    return render(request, 'inicio/servicio_iot.html')

def servicio_residuos(request):
    return render(request, 'inicio/servicio_residuos.html')

def servicio_bosque(request):
    return render(request, 'inicio/servicio_bosque.html')

def servicio_soc(request):
    return render(request, 'inicio/servicio_soc.html')

def blog(request):
    return render(request, 'inicio/blog.html')

def blog_parque_verde(request):
    return render(request, 'inicio/blog_parque_verde.html')

def blog_movilidad(request):
    return render(request, 'inicio/blog_movilidad.html')

def blog_lidar(request):
    return render(request, 'inicio/blog_lidar.html')

def blog_sav21(request):
    return render(request, 'inicio/blog_sav21.html')

from .models import Contacto

def contacto(request):
    success = False
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        organizacion = request.POST.get('organizacion', '')
        detalles = request.POST.get('detalles')
        
        if nombre and email and detalles:
            Contacto.objects.create(
                nombre_completo=nombre,
                email=email,
                organizacion=organizacion,
                detalles=detalles
            )
            success = True
            
    return render(request, 'inicio/contacto.html', {'success': success})

def catalogo(request):
    return render(request, 'inicio/catalogo.html')

def proyecto_movilidad(request):
    return render(request, 'inicio/proyecto_movilidad.html')

def proyecto_sustentabilidad(request):
    return render(request, 'inicio/proyecto_sustentabilidad.html')

def proyecto_iot(request):
    return render(request, 'inicio/proyecto_iot.html')

def proyecto_lidar(request):
    return render(request, 'inicio/proyecto_lidar.html')

def proyecto_saneamiento(request):
    return render(request, 'inicio/proyecto_saneamiento.html')

def proyecto_ciberseguridad(request):
    return render(request, 'inicio/proyecto_ciberseguridad.html')