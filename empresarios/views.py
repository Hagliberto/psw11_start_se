from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from .models import Empresas
from .validators import validar_cnpj
from django.shortcuts import render, get_object_or_404

# Cadastrar uma nova empresa
def cadastrar_empresa(request):
    # Verifica se o usuário está logado, se não, redireciona para a pagina de login
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    
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

        # Verificação da existência de escolhas válidas para 'tempo_existencia', 'estagio' e 'area'
        if tempo_existencia not in dict(Empresas.tempo_existencia_choices).keys():
            messages.add_message(request, constants.ERROR, 'Escolha um tempo de existência válido.')
            return redirect('/empresarios/cadastrar_empresa')

        if estagio not in dict(Empresas.estagio_choices).keys():
            messages.add_message(request, constants.ERROR, 'Escolha um estágio válido.')
            return redirect('/empresarios/cadastrar_empresa')

        if area not in dict(Empresas.area_choices).keys():
            messages.add_message(request, constants.ERROR, 'Escolha uma área válida.')
            return redirect('/empresarios/cadastrar_empresa')

        # Validação do arquivo 'pitch'
        if pitch:
            # Limite de tamanho de arquivo: 100MB
            if pitch.size > 100 * 1024 * 1024:
                messages.add_message(request, constants.ERROR, 'O arquivo pitch deve ter no máximo 100MB.')
                return redirect('/empresarios/cadastrar_empresa')

        # Validação do arquivo 'logo'
        if logo:
            # Verifica se o formato do arquivo é permitido (jpeg, png, jpg)
            if not logo.name.lower().endswith(('.jpeg', '.png', '.jpg')):
                messages.add_message(request, constants.ERROR, 'A logo deve estar nos formatos jpeg, png ou jpg.')
                return redirect('/empresarios/cadastrar_empresa')

        # Criação da empresa
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

# Listar empresas Cadastradas
def listar_empresas(request):
    # Verifica se o usuário está logado, se não, redireciona para a página de login
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')

    if request.method == "GET":
        # Inicia a query base, filtrando empresas do usuário logado
        empresas = Empresas.objects.filter(user=request.user)

        # Filtragem opcional com base nos parâmetros da query string
        nome = request.GET.get('nome')
        cnpj = request.GET.get('cnpj')
        tempo_existencia = request.GET.get('tempo_existencia')
        estagio = request.GET.get('estagio')
        area = request.GET.get('area')
        publico_alvo = request.GET.get('publico_alvo')
        valor_min = request.GET.get('valor_min')
        valor_max = request.GET.get('valor_max')

        # Aplica o filtro por nome da empresa, se fornecido
        if nome:
            empresas = empresas.filter(nome__icontains=nome)

        # Aplica o filtro por CNPJ, se fornecido
        if cnpj:
            empresas = empresas.filter(cnpj__icontains=cnpj)

        # Aplica o filtro por tempo de existência, se fornecido
        if tempo_existencia:
            empresas = empresas.filter(tempo_existencia=tempo_existencia)

        # Aplica o filtro por estágio, se fornecido
        if estagio:
            empresas = empresas.filter(estagio=estagio)

        # Aplica o filtro por área, se fornecido
        if area:
            empresas = empresas.filter(area=area)

        # Aplica o filtro por público-alvo, se fornecido
        if publico_alvo:
            empresas = empresas.filter(publico_alvo__icontains=publico_alvo)

        # Aplica o filtro por valor mínimo, se fornecido
        if valor_min:
            try:
                valor_min = float(valor_min)
                empresas = empresas.filter(valor__gte=valor_min)
            except ValueError:
                pass  # Se não for um valor numérico, ignora o filtro

        # Aplica o filtro por valor máximo, se fornecido
        if valor_max:
            try:
                valor_max = float(valor_max)
                empresas = empresas.filter(valor__lte=valor_max)
            except ValueError:
                pass  # Se não for um valor numérico, ignora o filtro

        # Renderiza a página com as empresas filtradas
        return render(request, 'listar_empresas.html', {'empresas': empresas})

# Detralhar empresas
def detalhar_empresa(request, id):
    empresa = get_object_or_404(Empresas, id=id)
    return render(request, 'detalhar_empresa.html', {'empresa': empresa})
