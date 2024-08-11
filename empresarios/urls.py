from django.urls import path
from . import views
urlpatterns = [
    path('cadastrar_empresa/', views.cadastrar_empresa, name="cadastrar_empresa"),
    path('listar_empresas/', views.listar_empresas, name="listar_empresas"),
    path('empresa/<int:id>/', views.detalhar_empresa, name='detalhar_empresa'),
    path('empresa/<int:id>', views.empresa, name="empresa"),
]
