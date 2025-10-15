"""
Módulo de gestão de colheitas
Capítulo 4: Estruturas de dados (listas, dicionários, tuplas)
"""

from datetime import datetime
from modulos.validacao import validar_data, validar_tipo_colheita, validar_producao, validar_perda
from modulos.fazenda import buscar_talhao
from config import TIPOS_PERDA


# Lista global de colheitas
colheitas = []


def criar_colheita(id_fazenda, codigo_talhao, data_colheita, tipo_colheita, 
                   quantidade_colhida, perdas_dict):
    """
    Cria um dicionário representando uma colheita
    
    Parâmetros:
        id_fazenda (int): ID da fazenda
        codigo_talhao (str): código do talhão
        data_colheita (str): data da colheita (DD/MM/AAAA)
        tipo_colheita (str): tipo (manual, mecânica, mista)
        quantidade_colhida (float): quantidade em toneladas
        perdas_dict (dict): dicionário com tipos de perda e percentuais
    
    Retorna:
        dict: dicionário com dados da colheita ou None se inválido
    """
    # Validações
    fazenda, talhao = buscar_talhao(id_fazenda, codigo_talhao)
    
    if not fazenda or not talhao:
        print("✗ Fazenda ou talhão não encontrado!")
        return None
    
    data = validar_data(data_colheita)
    if not data:
        return None
    
    if not validar_tipo_colheita(tipo_colheita):
        return None
    
    # Calcula produtividade
    area = talhao['area']
    produtividade = quantidade_colhida / area
    
    if not validar_producao(produtividade):
        return None
    
    # Valida perdas
    total_perdas = 0
    for tipo_perda, percentual in perdas_dict.items():
        if tipo_perda not in TIPOS_PERDA:
            print(f"⚠️ Tipo de perda '{tipo_perda}' não reconhecido")
            return None
        if not validar_perda(percentual):
            return None
        total_perdas += percentual
    
    # Calcula quantidade perdida
    quantidade_potencial = quantidade_colhida / (1 - total_perdas/100)
    quantidade_perdida = quantidade_potencial - quantidade_colhida
    
    # Cria tupla com resumo de perdas (imutável)
    resumo_perdas = tuple(sorted(perdas_dict.items(), key=lambda x: x[1], reverse=True))
    
    colheita = {
        'id': len(colheitas) + 1,
        'id_fazenda': id_fazenda,
        'nome_fazenda': fazenda['nome'],
        'codigo_talhao': codigo_talhao.upper(),
        'data_colheita': data_colheita,
        'data_registro': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'tipo_colheita': tipo_colheita.lower(),
        'area_colhida': area,
        'variedade': talhao['variedade'],
        'quantidade_colhida': round(quantidade_colhida, 2),
        'quantidade_perdida': round(quantidade_perdida, 2),
        'produtividade': round(produtividade, 2),
        'perdas_detalhadas': perdas_dict.copy(),  # cópia do dicionário
        'resumo_perdas': resumo_perdas,  # tupla ordenada
        'percentual_perda_total': round(total_perdas, 2),
        'status': classificar_perda(total_perdas)
    }
    
    return colheita


def classificar_perda(percentual_perda):
    """
    Classifica o nível de perda (usa tupla de parâmetros do config)
    
    Parâmetro:
        percentual_perda (float): percentual de perda
    
    Retorna:
        str: classificação da perda
    """
    from config import PARAMETROS_ANALISE
    
    for nome, limite in PARAMETROS_ANALISE:
        if percentual_perda <= limite:
            return nome.replace('_', ' ').upper()
    
    return "PERDA CRÍTICA"


def adicionar_colheita(colheita):
    """
    Adiciona uma colheita à lista de colheitas
    
    Parâmetro:
        colheita (dict): dicionário com dados da colheita
    
    Retorna:
        bool: True se adicionada com sucesso
    """
    if colheita:
        colheitas.append(colheita)
        print(f"\n✓ Colheita registrada com sucesso!")
        print(f"  ID: {colheita['id']}")
        print(f"  Fazenda: {colheita['nome_fazenda']}")
        print(f"  Talhão: {colheita['codigo_talhao']}")
        print(f"  Produtividade: {colheita['produtividade']} ton/ha")
        print(f"  Perda Total: {colheita['percentual_perda_total']}%")
        print(f"  Status: {colheita['status']}")
        return True
    return False


def buscar_colheita_por_id(id_colheita):
    """
    Busca uma colheita pelo ID
    
    Parâmetro:
        id_colheita (int): ID da colheita
    
    Retorna:
        dict: colheita encontrada ou None
    """
    for colheita in colheitas:
        if colheita['id'] == id_colheita:
            return colheita
    return None


def buscar_colheitas_fazenda(id_fazenda):
    """
    Busca todas as colheitas de uma fazenda
    
    Parâmetro:
        id_fazenda (int): ID da fazenda
    
    Retorna:
        list: lista de colheitas
    """
    return [c for c in colheitas if c['id_fazenda'] == id_fazenda]


def buscar_colheitas_talhao(id_fazenda, codigo_talhao):
    """
    Busca todas as colheitas de um talhão específico
    
    Parâmetros:
        id_fazenda (int): ID da fazenda
        codigo_talhao (str): código do talhão
    
    Retorna:
        list: lista de colheitas
    """
    return [c for c in colheitas 
            if c['id_fazenda'] == id_fazenda and c['codigo_talhao'] == codigo_talhao.upper()]


def buscar_colheitas_por_tipo(tipo_colheita):
    """
    Busca colheitas por tipo (manual, mecânica, mista)
    
    Parâmetro:
        tipo_colheita (str): tipo de colheita
    
    Retorna:
        list: lista de colheitas
    """
    return [c for c in colheitas if c['tipo_colheita'] == tipo_colheita.lower()]


def listar_colheitas():
    """
    Lista todas as colheitas cadastradas
    
    Retorna:
        list: lista de colheitas
    """
    return colheitas


def exibir_colheita_detalhada(colheita):
    """
    Exibe informações detalhadas de uma colheita
    Procedimento (não retorna valor)
    
    Parâmetro:
        colheita (dict): colheita a ser exibida
    """
    print("\n" + "="*70)
    print(f"COLHEITA #{colheita['id']}")
    print("="*70)
    print(f"Fazenda: {colheita['nome_fazenda']} (ID: {colheita['id_fazenda']})")
    print(f"Talhão: {colheita['codigo_talhao']} - {colheita['variedade']}")
    print(f"Data da Colheita: {colheita['data_colheita']}")
    print(f"Tipo: {colheita['tipo_colheita'].upper()}")
    print(f"Área Colhida: {colheita['area_colhida']} hectares")
    
    print(f"\n📊 PRODUÇÃO:")
    print(f"  Quantidade Colhida: {colheita['quantidade_colhida']:.2f} toneladas")
    print(f"  Produtividade: {colheita['produtividade']:.2f} ton/ha")
    
    print(f"\n⚠️ PERDAS:")
    print(f"  Quantidade Perdida: {colheita['quantidade_perdida']:.2f} toneladas")
    print(f"  Percentual Total: {colheita['percentual_perda_total']:.2f}%")
    print(f"  Status: {colheita['status']}")
    
    print(f"\n  Perdas Detalhadas:")
    for tipo_perda, percentual in colheita['resumo_perdas']:
        print(f"    • {tipo_perda.capitalize()}: {percentual:.2f}%")
    
    print(f"\nRegistro: {colheita['data_registro']}")
    print("="*70)


def obter_estatisticas_colheitas():
    """
    Retorna estatísticas das colheitas
    
    Retorna:
        dict: dicionário com estatísticas
    """
    if not colheitas:
        return {
            'total_colheitas': 0,
            'area_total_colhida': 0,
            'producao_total': 0,
            'perda_total': 0,
            'produtividade_media': 0,
            'perda_media': 0
        }
    
    area_total = sum(c['area_colhida'] for c in colheitas)
    producao_total = sum(c['quantidade_colhida'] for c in colheitas)
    perda_total = sum(c['quantidade_perdida'] for c in colheitas)
    
    produtividade_media = producao_total / area_total if area_total > 0 else 0
    
    # Calcula percentual médio de perda
    perda_media = sum(c['percentual_perda_total'] for c in colheitas) / len(colheitas)
    
    # Agrupa por tipo de colheita
    por_tipo = {}
    for c in colheitas:
        tipo = c['tipo_colheita']
        if tipo not in por_tipo:
            por_tipo[tipo] = {
                'quantidade': 0,
                'producao': 0,
                'area': 0,
                'perdas': []
            }
        por_tipo[tipo]['quantidade'] += 1
        por_tipo[tipo]['producao'] += c['quantidade_colhida']
        por_tipo[tipo]['area'] += c['area_colhida']
        por_tipo[tipo]['perdas'].append(c['percentual_perda_total'])
    
    # Calcula médias por tipo
    for tipo in por_tipo:
        dados = por_tipo[tipo]
        dados['produtividade_media'] = dados['producao'] / dados['area'] if dados['area'] > 0 else 0
        dados['perda_media'] = sum(dados['perdas']) / len(dados['perdas']) if dados['perdas'] else 0
    
    return {
        'total_colheitas': len(colheitas),
        'area_total_colhida': round(area_total, 2),
        'producao_total': round(producao_total, 2),
        'perda_total': round(perda_total, 2),
        'produtividade_media': round(produtividade_media, 2),
        'perda_media': round(perda_media, 2),
        'por_tipo': por_tipo
    }


def comparar_metodos_colheita():
    """
    Compara perdas entre métodos de colheita (manual vs mecânica)
    
    Retorna:
        dict: comparação entre métodos
    """
    manual = [c for c in colheitas if c['tipo_colheita'] == 'manual']
    mecanica = [c for c in colheitas if c['tipo_colheita'] == 'mecânica']
    
    def calcular_media(lista):
        if not lista:
            return 0
        return sum(c['percentual_perda_total'] for c in lista) / len(lista)
    
    return {
        'manual': {
            'quantidade': len(manual),
            'perda_media': round(calcular_media(manual), 2)
        },
        'mecanica': {
            'quantidade': len(mecanica),
            'perda_media': round(calcular_media(mecanica), 2)
        },
        'diferenca': round(calcular_media(mecanica) - calcular_media(manual), 2)
    }


def limpar_colheitas():
    """
    Remove todas as colheitas (útil para testes)
    """
    colheitas.clear()
    print("✓ Todas as colheitas foram removidas")


