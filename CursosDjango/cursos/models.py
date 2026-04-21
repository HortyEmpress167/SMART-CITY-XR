from django.db import models
from ckeditor.fields import RichTextField

class Servicio(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Servicio")
    descripcion_breve = models.CharField(max_length=200, verbose_name="Descripción Breve")
    descripcion_detallada = RichTextField(verbose_name="Descripción Detallada")
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Base")
    imagen = models.ImageField(upload_to='servicios_img/', verbose_name="Imagen Promocional", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['fecha_creacion']

    def __str__(self):
        return self.nombre

class Cotizacion(models.Model):
    ESTADOS_COTIZACION = [
        ('Pendiente', 'Pendiente de Revisión'),
        ('Evaluando', 'Evaluando Requisitos'),
        ('Contactado', 'Ciudadano Contactado'),
        ('Cerrado', 'Caso Cerrado'),
    ]
    ALCANCES = [
        ('Local', 'Nivel Local / Barrio'),
        ('Municipal', 'Nivel Municipal'),
        ('Estatal', 'Nivel Estatal / Nacional'),
    ]
    
    nombre_solicitante = models.CharField(max_length=150, verbose_name="Nombre del Solicitante")
    email = models.EmailField(verbose_name="Correo Electrónico")
    organizacion = models.CharField(max_length=150, verbose_name="Organización/Proyecto")
    detalles_solicitud = models.TextField(verbose_name="Detalles de la Solicitud")
    servicio_interes = models.CharField(max_length=150, null=True, blank=True, verbose_name="Servicio de Interés")
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    estado_cotizacion = models.CharField(max_length=20, choices=ESTADOS_COTIZACION, default='Pendiente', verbose_name="Estado Interno")
    alcance_proyecto = models.CharField(max_length=20, choices=ALCANCES, default='Local', verbose_name="Alcance del Proyecto")
    presupuesto_aprox = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Presupuesto Estimado ($)")

    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Cotización de {self.nombre_solicitante} - {self.organizacion}"

class ReporteProblema(models.Model):
    ESTADOS_REPORTE = [
        ('Recibido', 'Recibido por Sistema'),
        ('Revisión', 'En Revisión Analítica'),
        ('Desplegando', 'Desplegando Equipo/Dron'),
        ('Resuelto', 'Incidente Resuelto'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título del Problema")
    descripcion = models.TextField(verbose_name="Descripción o Detalles")
    votos = models.IntegerField(default=0, verbose_name="Cantidad de Votos")
    fecha_reporte = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Reporte")
    estado = models.CharField(max_length=20, choices=ESTADOS_REPORTE, default='Recibido', verbose_name="Estado Operativo")
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitud Geográfica")
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitud Geográfica")
    foto_evidencia = models.ImageField(upload_to='reportes_evidencia/', null=True, blank=True, verbose_name="Evidencia Visual")

    class Meta:
        verbose_name = "Reporte de Problema"
        verbose_name_plural = "Reportes Ciudadanos"
        ordering = ['-votos', '-fecha_reporte']

    def __str__(self):
        return f"{self.titulo} ({self.votos} votos)"
