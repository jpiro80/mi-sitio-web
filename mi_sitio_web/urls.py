from django.contrib import admin
from django.urls import path
from blog.views import lista_articulos, ArticuloListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lista_articulos, name='lista_articulos'),
    path('api/articulos/', ArticuloListAPIView.as_view(), name='api_articulos'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]