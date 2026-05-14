# Carreteras_Coord

Este proyecto implementa una aplicación Django para administrar ciudades y rutas, y permite buscar la mejor ruta entre dos ciudades usando una búsqueda similar a UCS/A\*.

## Estructura

- `carreteras/`: app Django con modelos `Ciudad` y `Ruta`, búsquedas y formulario de ruta.
- `coordenadas_project/`: configuración del proyecto Django.
- `requirements.txt`: dependencias del proyecto.

## Inicio rápido

1. Crea y activa un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Aplica migraciones:

```bash
python manage.py migrate
```

4. Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

5. Abre `http://127.0.0.1:8000/` en el navegador.

## Uso

- Agrega ciudades con coordenadas en `Agregar ciudad`.
- Agrega rutas entre ciudades en `Agregar ruta`.
- Usa `Buscar una ruta` para seleccionar origen y destino y ver la ruta calculada.

## Nota

El algoritmo usa un costo acumulado y una heurística basada en distancia geodésica entre coordenadas.
