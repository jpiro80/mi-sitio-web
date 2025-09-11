from django.test import TestCase
from django.urls import reverse
from .models import Articulo

class ArticuloTests(TestCase):

    def setUp(self):
        # Crea un objeto Articulo para usarlo en los tests.
        # Este método se ejecuta antes de cada test.
        Articulo.objects.create(titulo="Test Article", contenido="Test content")

    def test_articulo_creado(self):
        """Verifica que el artículo se ha creado correctamente."""
        articulo = Articulo.objects.get(titulo="Test Article")
        self.assertEqual(articulo.contenido, "Test content")

    def test_vista_lista_articulos(self):
        """Verifica que la vista de la lista de artículos funciona correctamente."""
        response = self.client.get(reverse('lista_articulos'))
        self.assertEqual(response.status_code, 200)

from rest_framework.test import APITestCase
from rest_framework import status

class ArticuloAPITests(APITestCase):
    def test_lista_articulos(self):
        """Verifica que el endpoint de la API de artículos retorna un HTTP 200 OK."""
        response = self.client.get('/api/articulos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)