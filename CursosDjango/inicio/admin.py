from django.contrib import admin
from .models import Contacto

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'organizacion', 'prioridad', 'atendido', 'fecha_envio')
    search_fields = ('nombre_completo', 'email', 'organizacion')
    list_filter = ('atendido', 'prioridad', 'fecha_envio')
    list_editable = ('prioridad', 'atendido')
    readonly_fields = ('fecha_envio',)

    fieldsets = (
        ('Datos de Contacto', {
            'fields': ('nombre_completo', 'email', 'organizacion')
        }),
        ('Mensaje Original', {
            'fields': ('detalles',)
        }),
        ('Seguimiento Interno (SOC)', {
            'fields': ('prioridad', 'atendido', 'notas_internas')
        }),
        ('Metadatos', {
            'fields': ('fecha_envio',),
            'classes': ('collapse',)
        }),
    )
