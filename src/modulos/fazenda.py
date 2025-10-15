"""
Módulo de gestão de fazendas e talhões
Capítulo 4: Estruturas de dados (listas, dicionários, tuplas)
"""

from datetime import datetime
from modulos.validacao import validar_cpf, validar_cnpj, validar_area, validar_variedade


# Lista global de fazendas (estrutura de dados principal)
fazendas = []


def criar_fazenda(nome, proprietario, cpf_cnpj, localizacao, area_total=0):
    """
    Cria um dicionário representando uma fazenda
    
    Parâmetros:
        nome (str): nome da fazenda
        proprietario (str): nome do proprietário
        cpf_cnpj (str): CPF ou CNPJ
        localizacao (str): cidade/estado
        area_total (float): área total em hectares
    
    Retorna:
        dict: dicionário com dados da fazenda
    """
    # Validação de CPF/CNPJ
    documento_limpo = cpf_cnpj.replace('.', '').replace('-', '').replace('/', '')
    
    if len(documento_limpo) == 11:
        if not validar_cpf(cpf_cnpj):
            print("✗ CPF inválido!")
            return None
        tipo_doc = 'CPF'
    elif len(documento_limpo) == 14:
        if not validar_cnpj(cpf_cnpj):
            print("✗ CNPJ inválido!")
            return None
        tipo_doc = 'CNPJ'
    else:
        print("✗ Documento inválido! Use CPF (11 dígitos) ou CNPJ (14 dígitos)")
        return None
    
    # Criação do dicionário de fazenda
    fazenda = {
        'id': len(fazendas) + 1,
        'nome': nome,
        'proprietario': proprietario,
        'documento': cpf_cnpj,
        'tipo_documento': tipo_doc,
        'localizacao': localizacao,
        'area_total': area_total,
        'talhoes': [],  # lista de talhões
        'data_cadastro': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    
    return fazenda


def adicionar_fazenda(fazenda):
    """
    Adiciona uma fazenda à lista de fazendas
    
    Parâmetro:
        fazenda (dict): dicionário com dados da fazenda
    
    Retorna:
        bool: True se adicionada com sucesso
    """
    if fazenda:
        fazendas.append(fazenda)
        print(f"\n✓ Fazenda '{fazenda['nome']}' cadastrada com sucesso!")
        print(f"  ID: {fazenda['id']}")
        return True
    return False


def buscar_fazenda_por_id(id_fazenda):
    """
    Busca uma fazenda pelo ID
    
    Parâmetro:
        id_fazenda (int): ID da fazenda
    
    Retorna:
        dict: fazenda encontrada ou None
    """
    for fazenda in fazendas:
        if fazenda['id'] == id_fazenda:
            return fazenda
    return None


def buscar_fazenda_por_nome(nome):
    """
    Busca fazendas pelo nome (busca parcial)
    
    Parâmetro:
        nome (str): nome ou parte do nome
    
    Retorna:
        list: lista de fazendas encontradas
    """
    encontradas = []
    for fazenda in fazendas:
        if nome.lower() in fazenda['nome'].lower():
            encontradas.append(fazenda)
    return encontradas


def criar_talhao(codigo, area, variedade, ano_plantio):
    """
    Cria um dicionário representando um talhão
    
    Parâmetros:
        codigo (str): código do talhão (ex: T01)
        area (float): área em hectares
        variedade (str): variedade de cana
        ano_plantio (int): ano do plantio
    
    Retorna:
        dict: dicionário com dados do talhão
    """
    if not validar_area(area):
        return None
    
    if not validar_variedade(variedade):
        return None
    
    # Tupla de coordenadas (exemplo - pode ser expandido)
    coordenadas = (0.0, 0.0)  # (latitude, longitude)
    
    talhao = {
        'codigo': codigo.upper(),
        'area': area,
        'variedade': variedade.upper(),
        'ano_plantio': ano_plantio,
        'coordenadas': coordenadas,  # tupla imutável
        'idade_anos': datetime.now().year - ano_plantio,
        'status': 'ativo'
    }
    
    return talhao


def adicionar_talhao_fazenda(id_fazenda, talhao):
    """
    Adiciona um talhão a uma fazenda específica
    
    Parâmetros:
        id_fazenda (int): ID da fazenda
        talhao (dict): dicionário do talhão
    
    Retorna:
        bool: True se adicionado com sucesso
    """
    fazenda = buscar_fazenda_por_id(id_fazenda)
    
    if not fazenda:
        print(f"✗ Fazenda ID {id_fazenda} não encontrada!")
        return False
    
    if not talhao:
        return False
    
    # Verifica se o código já existe
    for t in fazenda['talhoes']:
        if t['codigo'] == talhao['codigo']:
            print(f"✗ Já existe um talhão com o código '{talhao['codigo']}'!")
            return False
    
    fazenda['talhoes'].append(talhao)
    
    # Atualiza área total da fazenda
    fazenda['area_total'] = sum(t['area'] for t in fazenda['talhoes'])
    
    print(f"\n✓ Talhão '{talhao['codigo']}' adicionado à fazenda '{fazenda['nome']}'")
    print(f"  Área: {talhao['area']} ha")
    print(f"  Variedade: {talhao['variedade']}")
    print(f"  Área total da fazenda: {fazenda['area_total']} ha")
    
    return True


def buscar_talhao(id_fazenda, codigo_talhao):
    """
    Busca um talhão específico em uma fazenda
    
    Parâmetros:
        id_fazenda (int): ID da fazenda
        codigo_talhao (str): código do talhão
    
    Retorna:
        tuple: (fazenda, talhao) ou (None, None)
    """
    fazenda = buscar_fazenda_por_id(id_fazenda)
    
    if not fazenda:
        return None, None
    
    for talhao in fazenda['talhoes']:
        if talhao['codigo'] == codigo_talhao.upper():
            return fazenda, talhao
    
    return fazenda, None


def listar_fazendas():
    """
    Lista todas as fazendas cadastradas
    
    Retorna:
        list: lista de fazendas
    """
    return fazendas


def exibir_fazenda_detalhada(fazenda):
    """
    Exibe informações detalhadas de uma fazenda
    Procedimento (não retorna valor)
    
    Parâmetro:
        fazenda (dict): fazenda a ser exibida
    """
    print("\n" + "="*60)
    print(f"FAZENDA: {fazenda['nome']}")
    print("="*60)
    print(f"ID: {fazenda['id']}")
    print(f"Proprietário: {fazenda['proprietario']}")
    print(f"{fazenda['tipo_documento']}: {fazenda['documento']}")
    print(f"Localização: {fazenda['localizacao']}")
    print(f"Área Total: {fazenda['area_total']:.2f} hectares")
    print(f"Cadastro: {fazenda['data_cadastro']}")
    
    print(f"\nTalhões ({len(fazenda['talhoes'])}):")
    
    if fazenda['talhoes']:
        print("-" * 60)
        for talhao in fazenda['talhoes']:
            print(f"  • {talhao['codigo']}: {talhao['area']} ha - {talhao['variedade']}")
            print(f"    Plantio: {talhao['ano_plantio']} ({talhao['idade_anos']} anos)")
    else:
        print("  Nenhum talhão cadastrado")
    
    print("="*60)


def obter_estatisticas_fazendas():
    """
    Retorna estatísticas das fazendas cadastradas
    
    Retorna:
        dict: dicionário com estatísticas
    """
    if not fazendas:
        return {
            'total_fazendas': 0,
            'total_talhoes': 0,
            'area_total': 0,
            'variedades': {}
        }
    
    total_talhoes = sum(len(f['talhoes']) for f in fazendas)
    area_total = sum(f['area_total'] for f in fazendas)
    
    # Conta variedades (usando dicionário)
    variedades = {}
    for fazenda in fazendas:
        for talhao in fazenda['talhoes']:
            var = talhao['variedade']
            if var in variedades:
                variedades[var] += talhao['area']
            else:
                variedades[var] = talhao['area']
    
    return {
        'total_fazendas': len(fazendas),
        'total_talhoes': total_talhoes,
        'area_total': area_total,
        'variedades': variedades,
        'media_area_fazenda': area_total / len(fazendas) if fazendas else 0
    }


def limpar_fazendas():
    """
    Remove todas as fazendas (útil para testes)
    Procedimento que modifica a lista global
    """
    fazendas.clear()
    print("✓ Todas as fazendas foram removidas")


