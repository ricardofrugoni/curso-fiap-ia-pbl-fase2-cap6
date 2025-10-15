"""
Módulo de validação de dados
Contém funções para validar entradas do usuário
Capítulo 3: Subalgoritmos (funções com passagem de parâmetros)
"""

import re
from datetime import datetime
from config import LIMITES, TIPOS_COLHEITA, TIPOS_PERDA, VARIEDADES_CANA


def validar_inteiro(valor, mensagem="Digite um número inteiro: ", minimo=None, maximo=None):
    """
    Valida e retorna um número inteiro
    
    Parâmetros:
        valor: valor a ser validado (pode ser string ou int)
        mensagem: mensagem a exibir em caso de erro
        minimo: valor mínimo permitido
        maximo: valor máximo permitido
    
    Retorna:
        int: número validado ou None se inválido
    """
    try:
        num = int(valor)
        
        if minimo is not None and num < minimo:
            print(f"⚠️ Valor deve ser maior ou igual a {minimo}")
            return None
        
        if maximo is not None and num > maximo:
            print(f"⚠️ Valor deve ser menor ou igual a {maximo}")
            return None
        
        return num
    except ValueError:
        print(f"✗ Erro: {mensagem}")
        return None


def validar_float(valor, mensagem="Digite um número decimal: ", minimo=None, maximo=None):
    """
    Valida e retorna um número decimal (float)
    
    Parâmetros:
        valor: valor a ser validado
        mensagem: mensagem de erro
        minimo: valor mínimo
        maximo: valor máximo
    
    Retorna:
        float: número validado ou None se inválido
    """
    try:
        num = float(valor)
        
        if minimo is not None and num < minimo:
            print(f"⚠️ Valor deve ser maior ou igual a {minimo}")
            return None
        
        if maximo is not None and num > maximo:
            print(f"⚠️ Valor deve ser menor ou igual a {maximo}")
            return None
        
        return num
    except ValueError:
        print(f"✗ Erro: {mensagem}")
        return None


def validar_cpf(cpf):
    """
    Valida CPF (formato e dígitos verificadores)
    
    Parâmetro:
        cpf (str): CPF a ser validado
    
    Retorna:
        bool: True se válido, False caso contrário
    """
    # Remove caracteres especiais
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0
    
    if int(cpf[9]) != digito1:
        return False
    
    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0
    
    if int(cpf[10]) != digito2:
        return False
    
    return True


def validar_cnpj(cnpj):
    """
    Valida CNPJ (formato e dígitos verificadores)
    
    Parâmetro:
        cnpj (str): CNPJ a ser validado
    
    Retorna:
        bool: True se válido, False caso contrário
    """
    # Remove caracteres especiais
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return False
    
    # Validação do primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * multiplicadores1[i] for i in range(12))
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0
    
    if int(cnpj[12]) != digito1:
        return False
    
    # Validação do segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * multiplicadores2[i] for i in range(13))
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0
    
    if int(cnpj[13]) != digito2:
        return False
    
    return True


def validar_data(data_str):
    """
    Valida formato de data (DD/MM/AAAA)
    
    Parâmetro:
        data_str (str): data em formato string
    
    Retorna:
        datetime: objeto datetime se válido, None caso contrário
    """
    try:
        data = datetime.strptime(data_str, '%d/%m/%Y')
        
        # Verifica se a data não é futura
        if data > datetime.now():
            print("⚠️ A data não pode ser futura!")
            return None
        
        return data
    except ValueError:
        print("✗ Formato de data inválido! Use DD/MM/AAAA")
        return None


def validar_area(area):
    """
    Valida área em hectares
    
    Parâmetro:
        area (float): área em hectares
    
    Retorna:
        bool: True se válido, False caso contrário
    """
    if area < LIMITES['area_min'] or area > LIMITES['area_max']:
        print(f"⚠️ Área deve estar entre {LIMITES['area_min']} e {LIMITES['area_max']} hectares")
        return False
    return True


def validar_producao(producao_por_ha):
    """
    Valida produção em toneladas por hectare
    
    Parâmetro:
        producao_por_ha (float): produção em ton/ha
    
    Retorna:
        bool: True se válido, False caso contrário
    """
    if producao_por_ha < LIMITES['producao_min'] or producao_por_ha > LIMITES['producao_max']:
        print(f"⚠️ Produção deve estar entre {LIMITES['producao_min']} e {LIMITES['producao_max']} ton/ha")
        return False
    return True


def validar_perda(perda_percentual):
    """
    Valida percentual de perda
    
    Parâmetro:
        perda_percentual (float): perda em percentual
    
    Retorna:
        bool: True se válido, False caso contrário
    """
    if perda_percentual < LIMITES['perda_min'] or perda_percentual > LIMITES['perda_max']:
        print(f"⚠️ Perda deve estar entre {LIMITES['perda_min']}% e {LIMITES['perda_max']}%")
        return False
    return True


def validar_tipo_colheita(tipo):
    """
    Valida tipo de colheita (manual, mecânica, mista)
    
    Parâmetro:
        tipo (str): tipo de colheita
    
    Retorna:
        bool: True se válido, False caso contrário
    """
    if tipo.lower() not in TIPOS_COLHEITA:
        print(f"⚠️ Tipo de colheita deve ser um dos seguintes: {', '.join(TIPOS_COLHEITA)}")
        return False
    return True


def validar_variedade(variedade):
    """
    Valida variedade de cana
    
    Parâmetro:
        variedade (str): código da variedade
    
    Retorna:
        bool: True se válido, False caso contrário
    """
    if variedade.upper() not in VARIEDADES_CANA:
        print(f"⚠️ Variedade deve ser uma das seguintes: {', '.join(VARIEDADES_CANA)}")
        return False
    return True


def validar_string_nao_vazia(texto, nome_campo="Campo"):
    """
    Valida se uma string não está vazia
    
    Parâmetros:
        texto (str): texto a validar
        nome_campo (str): nome do campo para mensagem de erro
    
    Retorna:
        bool: True se válido, False caso contrário
    """
    if not texto or texto.strip() == "":
        print(f"⚠️ {nome_campo} não pode estar vazio!")
        return False
    return True


def obter_entrada_validada(tipo, mensagem, validacao_extra=None):
    """
    Obtém entrada do usuário com validação
    Função auxiliar que encapsula validação e entrada
    
    Parâmetros:
        tipo (str): tipo de dado ('int', 'float', 'str')
        mensagem (str): mensagem para o usuário
        validacao_extra (function): função adicional de validação
    
    Retorna:
        Valor validado do tipo especificado
    """
    while True:
        entrada = input(mensagem)
        
        if tipo == 'int':
            valor = validar_inteiro(entrada)
            if valor is not None:
                if validacao_extra is None or validacao_extra(valor):
                    return valor
        
        elif tipo == 'float':
            valor = validar_float(entrada)
            if valor is not None:
                if validacao_extra is None or validacao_extra(valor):
                    return valor
        
        elif tipo == 'str':
            if validar_string_nao_vazia(entrada):
                if validacao_extra is None or validacao_extra(entrada):
                    return entrada
        
        print("❌ Tente novamente.\n")


