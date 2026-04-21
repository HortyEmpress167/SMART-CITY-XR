from django import forms
from .models import ReporteProblema, Cotizacion

class ReporteProblemaForm(forms.ModelForm):
    class Meta:
        model = ReporteProblema
        fields = ['titulo', 'descripcion', 'latitud', 'longitud', 'foto_evidencia']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Baches en Zona Sur',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe el problema con detalle...',
                'rows': 4,
            }),
            'latitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Latitud (opcional)',
                'step': '0.000001',
            }),
            'longitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Longitud (opcional)',
                'step': '0.000001',
            }),
        }
        labels = {
            'titulo': 'Título del Incidente',
            'descripcion': 'Descripción Detallada',
            'latitud': 'Latitud GPS (opcional)',
            'longitud': 'Longitud GPS (opcional)',
            'foto_evidencia': 'Foto de Evidencia (opcional)',
        }

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = [
            'nombre_solicitante', 
            'email', 
            'organizacion', 
            'detalles_solicitud', 
            'servicio_interes', 
            'alcance_proyecto', 
            'presupuesto_aprox'
        ]
        widgets = {
            'nombre_solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'organizacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Empresa o Proyecto'}),
            'detalles_solicitud': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Cuéntanos sobre tu proyecto...', 'rows': 4}),
            'servicio_interes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Gemelo Digital, IoT...'}),
            'alcance_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'presupuesto_aprox': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto estimado (opcional)'}),
        }
        labels = {
            'nombre_solicitante': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'organizacion': 'Organización / Proyecto',
            'detalles_solicitud': 'Detalles de la Solicitud',
            'servicio_interes': 'Servicio de Interés',
            'alcance_proyecto': 'Alcance del Proyecto',
            'presupuesto_aprox': 'Presupuesto Estimado ($)',
        }
