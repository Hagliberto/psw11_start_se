"""
Configuração de URLs para o projeto core.

A lista `urlpatterns` mapeia URLs para as views. Para mais informações, consulte:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Exemplos:
Views baseadas em funções
    1. Adicione uma importação: from my_app import views
    2. Adicione uma URL ao urlpatterns: path('', views.home, name='home')
Views baseadas em classes
    1. Adicione uma importação: from other_app.views import Home
    2. Adicione uma URL ao urlpatterns: path('', Home.as_view(), name='home')
Incluindo outra configuração de URL (URLconf)
    1. Importe a função include(): from django.urls import include, path
    2. Adicione uma URL ao urlpatterns: path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# Lista de padrões de URL que mapeia as URLs para as views correspondentes
urlpatterns = [
    # Mapeia a URL 'admin/' para a interface administrativa do Django
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('empresarios/', include('empresarios.urls')),  
]
