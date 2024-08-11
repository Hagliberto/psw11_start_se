from django.shortcuts import render, redirect
from .models import Empresas
from django.contrib import messages
from django.contrib.messages import constants
import re

def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)  # Remove qualquer coisa que não seja número
    
    if len(cnpj) != 14:
        return False

    # Verifica se todos os dígitos são iguais, o que é um CNPJ inválido
    if cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj, peso):
        soma = sum(int(digito) * peso for digito, peso in zip(cnpj, peso))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)
    
    # Primeiro dígito verificador
    peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    primeiro_digito = calcular_digito(cnpj[:12], peso1)

    # Segundo dígito verificador
    peso2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    segundo_digito = calcular_digito(cnpj[:13], peso2)

    # Verifica se os dígitos calculados são iguais aos do CNPJ informado
    return cnpj[-2:] == primeiro_digito + segundo_digito

def cadastrar_empresa(request):
    if request.method == "GET":
        return render(request, 'cadastrar_empresa.html', {'tempo_existencia': Empresas.tempo_existencia_choices,
                                                          'areas': Empresas.area_choices})
    elif request.method == "POST":
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

        # Validações
        if not nome or not cnpj or not tempo_existencia or not descricao or not valor:
            messages.add_message(request, constants.ERROR, 'Todos os campos obrigatórios devem ser preenchidos.')
            return redirect('/empresarios/cadastrar_empresa')

        if not validar_cnpj(cnpj):
            messages.add_message(request, constants.ERROR, 'CNPJ inválido.')
            return redirect('/empresarios/cadastrar_empresa')

        try:
            valor = float(valor)
        except ValueError:
            messages.add_message(request, constants.ERROR, 'O valor deve ser numérico.')
            return redirect('/empresarios/cadastrar_empresa')

        try:
            percentual_equity = float(percentual_equity)
        except ValueError:
            messages.add_message(request, constants.ERROR, 'O percentual de equity deve ser numérico.')
            return redirect('/empresarios/cadastrar_empresa')

        # Criação da empresa
        try:
            empresa = Empresas(
                user=request.user,
                nome=nome,
                cnpj=cnpj,
                site=site,
                tempo_existencia=tempo_existencia,
                descricao=descricao,
                data_final_captacao=data_final,
                percentual_equity=percentual_equity,
                estagio=estagio,
                area=area,
                publico_alvo=publico_alvo,
                valor=valor,
                pitch=pitch,
                logo=logo
            )
            empresa.save()
        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Erro interno do servidor: {str(e)}')
            return redirect('/empresarios/cadastrar_empresa')

        messages.add_message(request, constants.SUCCESS, 'Empresa criada com sucesso')
        return redirect('/empresarios/cadastrar_empresa')
