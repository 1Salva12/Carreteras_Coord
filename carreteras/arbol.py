class Nodo:
    def __init__(self, datos, costo=None, padre=None):
        self._datos = datos
        self._costo = costo
        self._padre = padre
        self._hijos = []

    def get_datos(self):
        return self._datos

    def get_costo(self):
        return self._costo

    def set_costo(self, costo):
        self._costo = costo

    def get_padre(self):
        return self._padre

    def set_padre(self, padre):
        self._padre = padre

    def set_hijos(self, hijos):
        self._hijos = hijos

    def get_hijos(self):
        return self._hijos

    def igual(self, otro):
        return self._datos == otro.get_datos()

    def en_lista(self, lista_nodos):
        return any(self.igual(n) for n in lista_nodos)
