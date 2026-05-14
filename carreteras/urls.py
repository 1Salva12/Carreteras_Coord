from django.urls import path
from . import views

app_name = 'carreteras'

urlpatterns = [
    path('', views.index, name='index'),
]
