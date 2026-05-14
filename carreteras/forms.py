from django import forms
from .models import Ciudad


class CiudadForm(forms.ModelForm):
    coordenadas = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 20.139234509912956, -98.6735602490864'}),
        help_text='Ingresa latitud y longitud separadas por coma.'
    )

    class Meta:
        model = Ciudad
        fields = ['nombre', 'coordenadas']

    def clean_coordenadas(self):
        data = self.cleaned_data['coordenadas']
        try:
            lat, lon = data.split(',')
            lat = float(lat.strip())
            lon = float(lon.strip())
            return lat, lon
        except ValueError:
            raise forms.ValidationError('Formato inválido. Usa: latitud, longitud')

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat, lon = self.cleaned_data['coordenadas']
        instance.latitud = lat
        instance.longitud = lon
        if commit:
            instance.save()
        return instance
