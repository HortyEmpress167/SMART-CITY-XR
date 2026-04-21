from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Servicio, ReporteProblema, Cotizacion
from .forms import ReporteProblemaForm, CotizacionForm

# Create your views here.
def registros(request):
    servicios = Servicio.objects.all()  
    return render(request, "cursos/cursos.html", {'servicios': servicios})

from django.db.models import Sum

def lista_problemas(request):
    problemas = ReporteProblema.objects.all()
    total_reportes = problemas.count()
    total_votos = problemas.aggregate(Sum('votos'))['votos__sum'] or 0
    cnt_recibido   = problemas.filter(estado='Recibido').count()
    cnt_revision   = problemas.filter(estado='Revisión').count()
    cnt_desplegando = problemas.filter(estado='Desplegando').count()
    resueltos      = problemas.filter(estado='Resuelto').count()
    tasa_efectividad = int((resueltos / total_reportes * 100)) if total_reportes > 0 else 0

    context = {
        'problemas': problemas,
        'total_reportes': total_reportes,
        'total_votos': total_votos,
        'resueltos': resueltos,
        'tasa_efectividad': tasa_efectividad,
        'cnt_recibido': cnt_recibido,
        'cnt_revision': cnt_revision,
        'cnt_desplegando': cnt_desplegando,
    }
    return render(request, "cursos/lista_problemas.html", context)

def reportar_problema(request):
    if request.method == 'POST':
        form = ReporteProblemaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'reporte_enviado')
            return redirect('reportes:lista_problemas')
    else:
        form = ReporteProblemaForm()
    
    return render(request, "cursos/reportar.html", {'form': form})

def votar_problema(request, problema_id):
    problema = get_object_or_404(ReporteProblema, pk=problema_id)
    problema.votos += 1
    problema.save()
    messages.success(request, 'voto_registrado')
    return redirect('reportes:lista_problemas')

def solicitar_cotizacion(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'cotizacion_enviada')
            return redirect('inicio')
    else:
        form = CotizacionForm()
    
    return render(request, "cursos/solicitar_cotizacion.html", {'form': form})