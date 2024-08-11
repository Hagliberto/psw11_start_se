import re

# função responsável por validar CNPJs de forma eficaz, verificando tanto a estrutura quanto a consistência dos dígitos verificadores.
def validar_cnpj(cnpj):
    # Remove qualquer caractere que não seja número do CNPJ (como pontos, barras e hífens)
    cnpj = re.sub(r'\D', '', cnpj)  
    
    # Verifica se o CNPJ tem exatamente 14 dígitos
    if len(cnpj) != 14:
        return False

    # Verifica se todos os dígitos do CNPJ são iguais, o que é um indicativo de CNPJ inválido
    if cnpj == cnpj[0] * 14:
        return False

    # Função interna para calcular um dígito verificador
    def calcular_digito(cnpj, peso):
        # Calcula a soma dos produtos dos dígitos pelos seus respectivos pesos
        soma = sum(int(digito) * peso for digito, peso in zip(cnpj, peso))
        
        # Calcula o resto da divisão da soma por 11
        resto = soma % 11
        
        # Se o resto for menor que 2, o dígito verificador é 0, caso contrário, é 11 menos o resto
        return '0' if resto < 2 else str(11 - resto)
    
    # Lista de pesos usada para calcular o primeiro dígito verificador
    peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Calcula o primeiro dígito verificador usando os 12 primeiros dígitos do CNPJ e a lista de pesos
    primeiro_digito = calcular_digito(cnpj[:12], peso1)

    # Lista de pesos usada para calcular o segundo dígito verificador
    peso2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Calcula o segundo dígito verificador usando os 13 primeiros dígitos (12 dígitos mais o primeiro dígito verificador)
    segundo_digito = calcular_digito(cnpj[:13], peso2)

    # Verifica se os dois dígitos verificadores calculados são iguais aos dígitos verificadores do CNPJ informado
    return cnpj[-2:] == primeiro_digito + segundo_digito
