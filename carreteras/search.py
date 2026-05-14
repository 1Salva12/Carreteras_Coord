from math import sin, cos, acos
from .arbol import Nodo


def geodist(lat1, lon1, lat2, lon2):
    grad_rad = 0.01745329
    rad_grad = 57.29577951
    longitud = lon1 - lon2
    val = (sin(lat1 * grad_rad) * sin(lat2 * grad_rad)) + (
        cos(lat1 * grad_rad) * cos(lat2 * grad_rad) * cos(longitud * grad_rad)
    )
    if val > 1:
        val = 1
    if val < -1:
        val = -1
    return (acos(val) * rad_grad) * 111.32


def heuristica(ciudad, objetivo, coord):
    lat1, lon1 = coord[ciudad]
    lat2, lon2 = coord[objetivo]
    return int(geodist(lat1, lon1, lat2, lon2))


def compara(nodo, solucion, coord):
    costo_x = nodo.get_costo() if nodo.get_costo() is not None else 0
    return costo_x + heuristica(nodo.get_datos(), solucion, coord)


def buscar_solucion_USC(conexiones, coord, estado_inicial, solucion):
    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)
    nodos_frontera = [nodo_inicial]
    nodos_visitados = []

    while nodos_frontera:
        nodos_frontera.sort(key=lambda n: compara(n, solucion, coord))
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato_nodo = nodo.get_datos()
        lista_hijos = []
        for un_hijo, costo in conexiones.get(dato_nodo, {}).items():
            hijo = Nodo(un_hijo)
            hijo.set_costo(nodo.get_costo() + costo)
            hijo.set_padre(nodo)
            lista_hijos.append(hijo)

            if not hijo.en_lista(nodos_visitados):
                if hijo.en_lista(nodos_frontera):
                    for n in nodos_frontera:
                        if n.igual(hijo) and n.get_costo() > hijo.get_costo():
                            nodos_frontera.remove(n)
                            nodos_frontera.append(hijo)
                            break
                else:
                    nodos_frontera.append(hijo)
        nodo.set_hijos(lista_hijos)
    return None


def reconstruir_ruta(nodo):
    if nodo is None:
        return []
    ruta = []
    actual = nodo
    while actual is not None:
        ruta.append(actual.get_datos())
        actual = actual.get_padre()
    return list(reversed(ruta))
