from django.contrib import admin
from .models import Ciudad, Ruta


@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud')
    search_fields = ('nombre',)


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('origen', 'destino', 'distancia')
    list_filter = ('origen', 'destino')
    search_fields = ('origen__nombre', 'destino__nombre')
