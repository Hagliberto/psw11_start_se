from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from .models import Empresas
from .validators import validar_cnpj

def cadastrar_empresa(request):
    # Verifica se o método da requisição é GET
    if request.method == "GET":
        # Renderiza a página de cadastro de empresa com as opções de tempo de existência e áreas
        return render(request, 'cadastrar_empresa.html', {
            'tempo_existencia': Empresas.tempo_existencia_choices,
            'areas': Empresas.area_choices
        })
    
    # Verifica se o método da requisição é POST
    elif request.method == "POST":
        # Extrai os dados enviados no formulário
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        descricao = request.POST.get('descricao')
        data_final = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        # Validações de campos obrigatórios
        if not nome or not cnpj or not tempo_existencia or not descricao or not valor:
            messages.add_message(request, constants.ERROR, '⚠️ Todos os campos são obrigatórios e devem ser preenchidos.')
            return redirect('/empresarios/cadastrar_empresa')

        # Validação do CNPJ usando uma função externa
        if not validar_cnpj(cnpj):
            messages.add_message(request, constants.ERROR, 'CNPJ inválido.')
            return redirect('/empresarios/cadastrar_empresa')

        # Validação do campo 'valor', garantindo que seja um número
        try:
            valor = float(valor)
        except ValueError:
            messages.add_message(request, constants.ERROR, 'O valor deve ser numérico.')
            return redirect('/empresarios/cadastrar_empresa')

        # Validação do campo 'percentual_equity', garantindo que seja um número
        try:
            percentual_equity = float(percentual_equity)
        except ValueError:
            messages.add_message(request, constants.ERROR, 'O percentual de equity deve ser numérico.')
            return redirect('/empresarios/cadastrar_empresa')

        # Tentativa de criação da nova empresa
        try:
            empresa = Empresas(
                user=request.user,  # Atribui o usuário logado como o criador da empresa
                nome=nome,  # Nome da empresa
                cnpj=cnpj,  # CNPJ da empresa
                site=site,  # Site da empresa
                tempo_existencia=tempo_existencia,  # Tempo de existência da empresa
                descricao=descricao,  # Descrição da empresa
                data_final_captacao=data_final,  # Data final de captação
                percentual_equity=percentual_equity,  # Percentual de equity oferecido
                estagio=estagio,  # Estágio atual da empresa
                area=area,  # Área de atuação da empresa
                publico_alvo=publico_alvo,  # Público alvo da empresa
                valor=valor,  # Valor estimado da empresa
                pitch=pitch,  # Arquivo do pitch da empresa
                logo=logo  # Logo da empresa
            )
            empresa.save()  # Salva a empresa no banco de dados
        except Exception as e:
            # Captura qualquer exceção durante a criação da empresa e envia uma mensagem de erro
            messages.add_message(request, constants.ERROR, f'Erro interno do servidor: {str(e)}')
            return redirect('/empresarios/cadastrar_empresa')

        # Se tudo correr bem, envia uma mensagem de sucesso
        messages.add_message(request, constants.SUCCESS, '✅ Empresa criada com sucesso')
        return redirect('/empresarios/cadastrar_empresa')
