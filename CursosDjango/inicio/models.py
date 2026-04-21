from django.db import models
from ckeditor.fields import RichTextField

class Contacto(models.Model):
    PRIORIDADES = [
        ('Alta', 'Alta Prioridad'),
        ('Media', 'Prioridad Normal'),
        ('Baja', 'Baja Prioridad')
    ]

    nombre_completo = models.CharField(max_length=150)
    email = models.EmailField()
    organizacion = models.CharField(max_length=150, blank=True, null=True)
    detalles = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    
    atendido = models.BooleanField(default=False, verbose_name="¿Solicitud Atendida?")
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='Media', verbose_name="Nivel de Prioridad")
    notas_internas = RichTextField(blank=True, null=True, verbose_name="Notas del Operador (Internas)")

    def __str__(self):
        return f"{self.nombre_completo} - {self.email}"
