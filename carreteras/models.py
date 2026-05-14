from django.db import models


class Ciudad(models.Model):
    nombre = models.CharField(max_length=64, unique=True)
    latitud = models.FloatField()
    longitud = models.FloatField()

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return self.nombre


class Ruta(models.Model):
    origen = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name='rutas_origen')
    destino = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name='rutas_destino')
    distancia = models.FloatField(help_text='Distancia o costo entre ciudades')

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        unique_together = ('origen', 'destino')

    def __str__(self):
        return f'{self.origen} → {self.destino} ({self.distancia})'
