from django.shortcuts import render
from .models import Articulo
from rest_framework import generics
from .serializers import ArticuloSerializer
from django.views.decorators.cache import cache_page # Nuevo: Importa el decorador


class ArticuloListAPIView(generics.ListAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer

@cache_page(60 * 15)
def lista_articulos(request):
    articulos = Articulo.objects.all()
    contexto = {
        'articulos': articulos
    }
    return render(request, 'blog/lista_articulos.html', contexto)