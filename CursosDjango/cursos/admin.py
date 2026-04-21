from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import Servicio, Cotizacion, ReporteProblema

# ── Acciones masivas personalizadas ──────────────────────────────────────────

@admin.action(description='✔ Marcar seleccionados como RESUELTO')
def marcar_resuelto(modeladmin, request, queryset):
    updated = queryset.update(estado='Resuelto')
    modeladmin.message_user(request, f'✅ {updated} reporte(s) marcados como Resuelto.')

@admin.action(description='🚨 Escalar al SOC — Desplegando Equipo')
def escalar_soc(modeladmin, request, queryset):
    updated = queryset.update(estado='Desplegando')
    modeladmin.message_user(request, f'🚨 {updated} reporte(s) escalados a Desplegando.')

@admin.action(description='🔍 Poner En Revisión Analítica')
def poner_en_revision(modeladmin, request, queryset):
    updated = queryset.update(estado='Revisión')
    modeladmin.message_user(request, f'🔍 {updated} reporte(s) enviados a Revisión.')

@admin.action(description='📥 Restablecer a Recibido')
def restablecer_recibido(modeladmin, request, queryset):
    updated = queryset.update(estado='Recibido')
    modeladmin.message_user(request, f'📥 {updated} reporte(s) restablecidos a Recibido.')

# ── Admins ────────────────────────────────────────────────────────────────────

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    list_display = ('nombre', 'descripcion_breve', 'precio_base')
    search_fields = ('nombre', 'descripcion_breve')
    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', 'descripcion_breve', 'precio_base', 'imagen')
        }),
        ('Detalles', {
            'fields': ('descripcion_detallada',)
        }),
        ('Metadatos de Sistema', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_solicitud',)
    list_display = ('nombre_solicitante', 'organizacion', 'servicio_interes', 'estado_cotizacion', 'alcance_proyecto', 'fecha_solicitud')
    search_fields = ('nombre_solicitante', 'organizacion', 'email')
    list_filter = ('estado_cotizacion', 'alcance_proyecto', 'servicio_interes')
    list_editable = ('estado_cotizacion', 'alcance_proyecto')
    fieldsets = (
        ('Datos del Solicitante', {
            'fields': ('nombre_solicitante', 'email', 'organizacion')
        }),
        ('Detalles del Proyecto', {
            'fields': ('servicio_interes', 'detalles_solicitud', 'alcance_proyecto', 'presupuesto_aprox')
        }),
        ('Gestión Administrativa', {
            'fields': ('estado_cotizacion', 'fecha_solicitud')
        }),
    )


# ── ReporteProblema con estadísticas en vivo ─────────────────────────────────

@admin.register(ReporteProblema)
class ReporteProblemaAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_reporte', 'resumen_estadisticas')
    list_display = ('titulo', 'estado_badge', 'estado', 'votos_badge', 'fecha_reporte', 'tiene_gps', 'tiene_foto')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('estado', 'fecha_reporte')
    list_editable = ('estado',)
    list_per_page = 20
    actions = [marcar_resuelto, escalar_soc, poner_en_revision, restablecer_recibido]

    # ── Columna: Badge de estado con colores ──────────────────────────────────
    @admin.display(description='Estado Visual')
    def estado_badge(self, obj):
        estilos = {
            'Resuelto':    ('#00f5d4', '✔'),
            'Desplegando': ('#f59e0b', '🚨'),
            'Revisión':    ('#00b4ff', '🔍'),
            'Recibido':    ('#00e5ff', '📡'),
        }
        color, icono = estilos.get(obj.estado, ('#ffffff', '?'))
        return format_html(
            '<span style="display:inline-block;padding:3px 10px;border-radius:20px;'
            'background:{color}22;border:1px solid {color};color:{color};'
            'font-weight:bold;font-size:0.78rem;">{icono} {estado}</span>',
            color=color, icono=icono, estado=obj.estado
        )

    # ── Columna: Contador de votos con color dinámico ─────────────────────────
    @admin.display(description='Votos 👍')
    def votos_badge(self, obj):
        color = '#32cd32' if obj.votos >= 5 else ('#f59e0b' if obj.votos >= 2 else '#aaaaaa')
        return format_html(
            '<b style="color:{};font-size:1.1rem;">{}</b>',
            color, obj.votos
        )

    @admin.display(description='GPS', boolean=True)
    def tiene_gps(self, obj):
        return obj.latitud is not None

    @admin.display(description='Foto', boolean=True)
    def tiene_foto(self, obj):
        return bool(obj.foto_evidencia)

    # ── Campo readonly: Panel de estadísticas en vivo ─────────────────────────
    @admin.display(description='📊 Panel de Estadísticas en Vivo')
    def resumen_estadisticas(self, obj):
        qs = ReporteProblema.objects.all()
        total        = qs.count()
        total_votos  = qs.aggregate(Sum('votos'))['votos__sum'] or 0
        recibidos    = qs.filter(estado='Recibido').count()
        en_revision  = qs.filter(estado='Revisión').count()
        desplegando  = qs.filter(estado='Desplegando').count()
        resueltos    = qs.filter(estado='Resuelto').count()
        tasa         = int(resueltos / total * 100) if total > 0 else 0

        return format_html('''
            <div style="font-family:monospace;background:#0d1117;border:1px solid #30363d;
                        border-radius:10px;padding:18px;max-width:520px;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
                <div style="color:#58a6ff;font-weight:bold;margin-bottom:14px;font-size:0.85rem;
                            letter-spacing:1.5px;border-bottom:1px solid #21262d;padding-bottom:10px;">
                    ⚡ TELEMETRÍA DE PARTICIPACIÓN CIUDADANA
                    <span style="float:right;color:#8b949e;font-weight:normal;font-size:0.75rem;">actualiza al guardar</span>
                </div>
                <table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
                    <tr>
                        <td style="padding:5px 0;color:#8b949e;">📡 Total Reportes</td>
                        <td style="text-align:right;color:#e6edf3;font-weight:bold;font-size:1rem;">{total}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0;color:#8b949e;">👆 Votos Ciudadanos</td>
                        <td style="text-align:right;color:#32cd32;font-weight:bold;font-size:1.1rem;">{votos}</td>
                    </tr>
                    <tr><td colspan="2"><div style="border-top:1px solid #21262d;margin:8px 0;"></div></td></tr>
                    <tr>
                        <td style="padding:5px 0;"><span style="background:#00e5ff22;border:1px solid #00e5ff;
                            color:#00e5ff;border-radius:20px;padding:2px 8px;font-size:0.75rem;">📡 Recibido</span></td>
                        <td style="text-align:right;color:#00e5ff;font-weight:bold;">{recibidos}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0;"><span style="background:#00b4ff22;border:1px solid #00b4ff;
                            color:#00b4ff;border-radius:20px;padding:2px 8px;font-size:0.75rem;">🔍 En Revisión</span></td>
                        <td style="text-align:right;color:#00b4ff;font-weight:bold;">{revision}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0;"><span style="background:#f59e0b22;border:1px solid #f59e0b;
                            color:#f59e0b;border-radius:20px;padding:2px 8px;font-size:0.75rem;">🚨 Desplegando</span></td>
                        <td style="text-align:right;color:#f59e0b;font-weight:bold;">{desplegando}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0;"><span style="background:#00f5d422;border:1px solid #00f5d4;
                            color:#00f5d4;border-radius:20px;padding:2px 8px;font-size:0.75rem;">✔ Resuelto</span></td>
                        <td style="text-align:right;color:#00f5d4;font-weight:bold;">{resueltos}</td>
                    </tr>
                </table>
                <div style="border-top:1px solid #21262d;margin:10px 0 8px;"></div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="color:#8b949e;font-size:0.8rem;">⚡ Efectividad de Resolución</span>
                    <span style="color:#00f5d4;font-weight:bold;font-size:1rem;">{tasa}%</span>
                </div>
                <div style="background:#161b22;border-radius:4px;height:8px;overflow:hidden;border:1px solid #30363d;">
                    <div style="width:{tasa}%;height:100%;
                                background:linear-gradient(90deg,#00b4ff,#00f5d4);border-radius:4px;
                                box-shadow:0 0 8px rgba(0,245,212,0.5);"></div>
                </div>
                <p style="color:#8b949e;font-size:0.72rem;margin-top:8px;margin-bottom:0;">
                    ℹ️ Cambia el estado de cualquier reporte y presiona <strong style="color:#58a6ff;">Guardar</strong> para ver reflejados los cambios en el panel ciudadano.
                </p>
            </div>
        ''', total=total, votos=total_votos, recibidos=recibidos,
             revision=en_revision, desplegando=desplegando,
             resueltos=resueltos, tasa=tasa)

    # ── Fieldsets del formulario de edición ───────────────────────────────────
    fieldsets = (
        ('📊 Panel de Estadísticas en Vivo', {
            'fields': ('resumen_estadisticas',),
            'description': (
                'Este panel refleja exactamente los datos que verán los ciudadanos en la web. '
                'Cambia el estado de este reporte y guarda para actualizar el dashboard público.'
            ),
        }),
        ('📋 Información del Incidente', {
            'fields': ('titulo', 'descripcion', 'foto_evidencia'),
        }),
        ('⚙️ Gestión Operativa', {
            'fields': ('estado', 'votos', 'latitud', 'longitud'),
            'description': '⚠️ Cambiar "Estado" aquí actualiza automáticamente las gráficas del panel ciudadano.',
        }),
        ('🗂️ Metadatos', {
            'fields': ('fecha_reporte',),
            'classes': ('collapse',),
        }),
    )
