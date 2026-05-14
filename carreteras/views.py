from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CiudadForm
from .models import Ciudad, Ruta
from .search import buscar_solucion_USC, reconstruir_ruta, geodist

DEFAULT_CIUDADES = {
    'jiloyork': (19.952704139636957, -99.53317473760144),
    'CDMX': (19.432899920229252, -99.13333032071326),
    'QRO': (21.86108909244176, -102.32107525105744),
    'MORELOS': (18.922479742463228, -99.2350167584074),
    'SONORA': (29.072671034584083, -110.95649770433667),
    'AGS': (21.86125231158153, -102.32115086294898),
    'MONTERREY': (25.67882050049562, -100.28420130516906),
    'SLP': (22.38568493986999, -100.96514265832738),
    'HGO': (20.139234509912956, -98.6735602490864),
    'MEXICALI': (32.6278, -115.4545),
}

DEFAULT_RUTAS = [
    ('jiloyork', 'CDMX', 125),
    ('jiloyork', 'QRO', 513),
    ('MORELOS', 'QRO', 524),
    ('CDMX', 'QRO', 433),
    ('CDMX', 'HGO', 401),
    ('HGO', 'QRO', 356),
    ('HGO', 'MEXICALI', 309),
    ('HGO', 'MONTERREY', 346),
    ('QRO', 'SLP', 203),
    ('QRO', 'MONTERREY', 603),
    ('QRO', 'SONORA', 437),
    ('QRO', 'MEXICALI', 313),
    ('QRO', 'AGS', 599),
    ('SLP', 'AGS', 390),
    ('SONORA', 'MEXICALI', 394),
    ('MEXICALI', 'MONTERREY', 296),
]


def cargar_datos_iniciales():
    nombres_existentes = set(Ciudad.objects.values_list('nombre', flat=True))
    if set(DEFAULT_CIUDADES) <= nombres_existentes and Ruta.objects.exists():
        return

    ciudades_obj = {}
    for nombre, (latitud, longitud) in DEFAULT_CIUDADES.items():
        ciudad, _ = Ciudad.objects.get_or_create(
            nombre=nombre,
            defaults={'latitud': latitud, 'longitud': longitud}
        )
        if ciudad.latitud != latitud or ciudad.longitud != longitud:
            ciudad.latitud = latitud
            ciudad.longitud = longitud
            ciudad.save()
        ciudades_obj[nombre] = ciudad

    for origen, destino, distancia in DEFAULT_RUTAS:
        ciudad_origen = ciudades_obj[origen]
        ciudad_destino = ciudades_obj[destino]
        if not Ruta.objects.filter(origen=ciudad_origen, destino=ciudad_destino).exists():
            Ruta.objects.create(origen=ciudad_origen, destino=ciudad_destino, distancia=distancia)


def index(request):
    cargar_datos_iniciales()
    error = None
    resultado = None
    costo = None
    origen_sel = None
    destino_sel = None

    ciudad_form = CiudadForm()

    if request.method == 'POST' and 'add_city' in request.POST:
        ciudad_form = CiudadForm(request.POST)
        if ciudad_form.is_valid():
            ciudad = ciudad_form.save()
            for otra in Ciudad.objects.exclude(pk=ciudad.pk):
                distancia = int(geodist(ciudad.latitud, ciudad.longitud, otra.latitud, otra.longitud))
                if not Ruta.objects.filter(origen=ciudad, destino=otra).exists() and not Ruta.objects.filter(origen=otra, destino=ciudad).exists():
                    Ruta.objects.create(origen=ciudad, destino=otra, distancia=distancia)
            return redirect(reverse('carreteras:index'))

    if request.method == 'GET' and 'origen' in request.GET and 'destino' in request.GET:
        origen_sel = request.GET.get('origen')
        destino_sel = request.GET.get('destino')
        ciudades = Ciudad.objects.order_by('nombre')
        nombres = [ciudad.nombre for ciudad in ciudades]
        if origen_sel not in nombres or destino_sel not in nombres:
            error = 'Selecciona un origen y un destino válidos.'
        elif origen_sel == destino_sel:
            error = 'Origen y destino deben ser diferentes.'
        else:
            coord = {ciudad.nombre: (ciudad.latitud, ciudad.longitud) for ciudad in ciudades}
            conexiones = {}
            for ruta in Ruta.objects.all():
                conexiones.setdefault(ruta.origen.nombre, {})[ruta.destino.nombre] = ruta.distancia
                conexiones.setdefault(ruta.destino.nombre, {})[ruta.origen.nombre] = ruta.distancia

            nodo_solucion = buscar_solucion_USC(conexiones, coord, origen_sel, destino_sel)
            if nodo_solucion:
                resultado = reconstruir_ruta(nodo_solucion)
                costo = nodo_solucion.get_costo()
            else:
                error = 'No se encontró una ruta entre las ciudades seleccionadas.'

    ciudades = Ciudad.objects.order_by('nombre')
    rutas = Ruta.objects.select_related('origen', 'destino').order_by('origen__nombre', 'destino__nombre')
    return render(request, 'carreteras/index.html', {
        'ciudades': ciudades,
        'rutas': rutas,
        'ciudad_form': ciudad_form,
        'resultado': resultado,
        'costo': costo,
        'error': error,
        'origen_sel': origen_sel,
        'destino_sel': destino_sel,
    })
