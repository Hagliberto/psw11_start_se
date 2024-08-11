from django.urls import path
from . import views

urlpatterns = [
    # Rota para cadastrar uma nova empresa
    path('cadastrar_empresa/', views.cadastrar_empresa, name="cadastrar_empresa"),
    
    # Rota para listar todas as empresas
    path('listar_empresas/', views.listar_empresas, name="listar_empresas"),
    
    # # Rota para detalhar uma empresa específica pelo ID
    # path('empresa/<int:id>/', views.detalhar_empresa, name='detalhar_empresa'),
    
    # Rota para exibir informações de uma empresa específica pelo ID
    path('empresa/<int:id>/', views.empresa, name="empresa"),
    
    # Rota para adicionar um documento a uma empresa específica pelo ID
    path('add_doc/<int:id>/', views.add_doc, name="add_doc"),
    
    # Rota para excluir um documento de um empresa específica pelo ID
    path('excluir_dc/<int:id>', views.excluir_dc, name="excluir_dc"),

    # Rota para métricas
    path('add_metrica/<int:id>', views.add_metrica, name="add_metrica"),



]
