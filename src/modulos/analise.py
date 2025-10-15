"""
Módulo de análise e recomendações
Capítulo 4: Estruturas de dados avançadas (tabelas de memória, análises)
"""

from modulos.colheita import colheitas, comparar_metodos_colheita
from modulos.fazenda import fazendas
from config import PRODUTIVIDADE_ESPERADA, PARAMETROS_ANALISE


def gerar_tabela_desempenho():
    """
    Gera uma tabela (matriz) de desempenho das colheitas
    Estrutura de dados: lista de listas (tabela de memória)
    
    Retorna:
        list: tabela com dados de desempenho
    """
    # Cabeçalho da tabela
    tabela = [
        ['ID', 'Fazenda', 'Talhão', 'Tipo', 'Prod.(t/ha)', 'Perda(%)', 'Status']
    ]
    
    for colheita in colheitas:
        linha = [
            colheita['id'],
            colheita['nome_fazenda'][:20],  # limita o tamanho
            colheita['codigo_talhao'],
            colheita['tipo_colheita'][:3].upper(),
            f"{colheita['produtividade']:.1f}",
            f"{colheita['percentual_perda_total']:.1f}",
            obter_icone_status(colheita['percentual_perda_total'])
        ]
        tabela.append(linha)
    
    return tabela


def obter_icone_status(percentual_perda):
    """
    Retorna um ícone de status baseado no percentual de perda
    
    Parâmetro:
        percentual_perda (float): percentual de perda
    
    Retorna:
        str: ícone de status
    """
    if percentual_perda <= 5:
        return "✓ ÓTIMO"
    elif percentual_perda <= 10:
        return "⚠️ BOM"
    elif percentual_perda <= 15:
        return "⚠️ ATENÇÃO"
    else:
        return "❌ CRÍTICO"


def exibir_tabela(tabela):
    """
    Exibe uma tabela formatada no console
    Procedimento que imprime a tabela
    
    Parâmetro:
        tabela (list): lista de listas representando a tabela
    """
    if not tabela or len(tabela) <= 1:
        print("Nenhum dado para exibir")
        return
    
    # Calcula largura das colunas
    larguras = []
    for i in range(len(tabela[0])):
        largura_max = max(len(str(linha[i])) for linha in tabela)
        larguras.append(largura_max + 2)
    
    # Imprime cabeçalho
    print("\n" + "="*sum(larguras))
    cabecalho = tabela[0]
    linha_cabecalho = ""
    for i, valor in enumerate(cabecalho):
        linha_cabecalho += str(valor).ljust(larguras[i])
    print(linha_cabecalho)
    print("="*sum(larguras))
    
    # Imprime dados
    for linha in tabela[1:]:
        linha_formatada = ""
        for i, valor in enumerate(linha):
            linha_formatada += str(valor).ljust(larguras[i])
        print(linha_formatada)
    
    print("="*sum(larguras))
    print(f"Total de registros: {len(tabela) - 1}")


def analisar_produtividade_por_variedade():
    """
    Analisa produtividade por variedade de cana
    
    Retorna:
        dict: análise por variedade
    """
    analise = {}
    
    for colheita in colheitas:
        variedade = colheita['variedade']
        
        if variedade not in analise:
            analise[variedade] = {
                'colheitas': [],
                'producao_total': 0,
                'area_total': 0,
                'perdas': []
            }
        
        analise[variedade]['colheitas'].append(colheita['id'])
        analise[variedade]['producao_total'] += colheita['quantidade_colhida']
        analise[variedade]['area_total'] += colheita['area_colhida']
        analise[variedade]['perdas'].append(colheita['percentual_perda_total'])
    
    # Calcula médias e comparações
    for variedade in analise:
        dados = analise[variedade]
        dados['produtividade_media'] = dados['producao_total'] / dados['area_total'] if dados['area_total'] > 0 else 0
        dados['perda_media'] = sum(dados['perdas']) / len(dados['perdas']) if dados['perdas'] else 0
        dados['num_colheitas'] = len(dados['colheitas'])
        
        # Compara com produtividade esperada
        if variedade in PRODUTIVIDADE_ESPERADA:
            esperado = PRODUTIVIDADE_ESPERADA[variedade]
            dados['produtividade_esperada'] = esperado
            dados['diferenca_esperado'] = dados['produtividade_media'] - esperado
            dados['percentual_esperado'] = (dados['produtividade_media'] / esperado * 100) if esperado > 0 else 0
        else:
            dados['produtividade_esperada'] = None
            dados['diferenca_esperado'] = None
            dados['percentual_esperado'] = None
    
    return analise


def identificar_talhoes_criticos():
    """
    Identifica talhões com maiores perdas
    
    Retorna:
        list: lista de tuplas (fazenda, talhão, perda_media, num_colheitas)
    """
    # Agrupa colheitas por talhão
    talhoes = {}
    
    for colheita in colheitas:
        chave = (colheita['id_fazenda'], colheita['codigo_talhao'])
        
        if chave not in talhoes:
            talhoes[chave] = {
                'nome_fazenda': colheita['nome_fazenda'],
                'perdas': [],
                'colheitas': 0
            }
        
        talhoes[chave]['perdas'].append(colheita['percentual_perda_total'])
        talhoes[chave]['colheitas'] += 1
    
    # Calcula média de perdas e cria tuplas
    resultado = []
    for (id_fazenda, codigo_talhao), dados in talhoes.items():
        perda_media = sum(dados['perdas']) / len(dados['perdas'])
        tupla = (dados['nome_fazenda'], codigo_talhao, round(perda_media, 2), dados['colheitas'])
        resultado.append(tupla)
    
    # Ordena por perda média (decrescente)
    resultado.sort(key=lambda x: x[2], reverse=True)
    
    return resultado


def gerar_recomendacoes(colheita):
    """
    Gera recomendações baseadas nos dados de uma colheita
    
    Parâmetro:
        colheita (dict): dicionário da colheita
    
    Retorna:
        list: lista de recomendações (strings)
    """
    recomendacoes = []
    
    # Análise de perda total
    perda_total = colheita['percentual_perda_total']
    
    if perda_total > 15:
        recomendacoes.append("🚨 URGENTE: Perdas críticas! Requer ação imediata.")
    elif perda_total > 10:
        recomendacoes.append("⚠️ Perdas acima da média. Revisar processo de colheita.")
    elif perda_total <= 5:
        recomendacoes.append("✓ Excelente desempenho! Manter práticas atuais.")
    
    # Análise por tipo de perda
    perdas = colheita['perdas_detalhadas']
    
    if 'mecânica' in perdas and perdas['mecânica'] > 5:
        recomendacoes.append("🔧 Revisar regulagem da colheitadeira (velocidade, altura de corte).")
        recomendacoes.append("📋 Verificar manutenção preventiva do equipamento.")
    
    if 'raizame' in perdas and perdas['raizame'] > 3:
        recomendacoes.append("🌱 Ajustar altura de corte para evitar arrancamento de raízes.")
    
    if 'palha' in perdas and perdas['palha'] > 3:
        recomendacoes.append("🍂 Otimizar sistema de limpeza e extração da palha.")
    
    if 'climática' in perdas and perdas['climática'] > 2:
        recomendacoes.append("🌦️ Planejar colheita em períodos mais favoráveis.")
        recomendacoes.append("📅 Considerar sistema de monitoramento meteorológico.")
    
    if 'pragas' in perdas and perdas['pragas'] > 2:
        recomendacoes.append("🐛 Implementar controle integrado de pragas.")
        recomendacoes.append("🔬 Realizar análise fitossanitária do talhão.")
    
    # Análise de tipo de colheita
    if colheita['tipo_colheita'] == 'mecânica' and perda_total > 10:
        recomendacoes.append("👨‍🌾 Considerar colheita manual em talhões críticos.")
        recomendacoes.append("📊 Comparar custo-benefício entre métodos de colheita.")
    
    # Análise de produtividade
    variedade = colheita['variedade']
    if variedade in PRODUTIVIDADE_ESPERADA:
        esperado = PRODUTIVIDADE_ESPERADA[variedade]
        if colheita['produtividade'] < esperado * 0.8:  # 80% do esperado
            recomendacoes.append(f"📉 Produtividade abaixo do esperado para {variedade}.")
            recomendacoes.append("🌾 Revisar manejo do talhão (adubação, irrigação).")
    
    # Se não houver recomendações específicas
    if not recomendacoes:
        recomendacoes.append("✓ Operação dentro dos parâmetros normais.")
        recomendacoes.append("💡 Continuar monitoramento regular.")
    
    return recomendacoes


def gerar_dashboard():
    """
    Gera um dashboard com indicadores principais
    Procedimento que exibe informações consolidadas
    """
    print("\n" + "="*70)
    print(" "*20 + "📊 DASHBOARD - GESTÃO DE COLHEITAS")
    print("="*70)
    
    if not colheitas:
        print("\nℹ️ Nenhuma colheita registrada ainda.")
        print("="*70)
        return
    
    # Estatísticas gerais
    total_colheitas = len(colheitas)
    producao_total = sum(c['quantidade_colhida'] for c in colheitas)
    perda_total = sum(c['quantidade_perdida'] for c in colheitas)
    area_total = sum(c['area_colhida'] for c in colheitas)
    
    print(f"\n📈 INDICADORES GERAIS:")
    print(f"  • Total de Colheitas: {total_colheitas}")
    print(f"  • Produção Total: {producao_total:.2f} toneladas")
    print(f"  • Área Total Colhida: {area_total:.2f} hectares")
    print(f"  • Produtividade Média: {(producao_total/area_total):.2f} ton/ha")
    print(f"  • Perda Total: {perda_total:.2f} toneladas")
    
    # Comparação de métodos
    comparacao = comparar_metodos_colheita()
    
    print(f"\n⚖️ COMPARAÇÃO DE MÉTODOS:")
    print(f"  • Manual: {comparacao['manual']['quantidade']} colheitas - "
          f"Perda média: {comparacao['manual']['perda_media']}%")
    print(f"  • Mecânica: {comparacao['mecanica']['quantidade']} colheitas - "
          f"Perda média: {comparacao['mecanica']['perda_media']}%")
    print(f"  • Diferença: {comparacao['diferenca']}% "
          f"({'maior' if comparacao['diferenca'] > 0 else 'menor'} na mecânica)")
    
    # Distribuição por status
    status_count = {}
    for c in colheitas:
        status = c['status']
        status_count[status] = status_count.get(status, 0) + 1
    
    print(f"\n📊 DISTRIBUIÇÃO POR STATUS:")
    for status, count in sorted(status_count.items()):
        percentual = (count / total_colheitas) * 100
        print(f"  • {status}: {count} ({percentual:.1f}%)")
    
    # Talhões críticos
    criticos = identificar_talhoes_criticos()[:3]  # Top 3
    
    if criticos:
        print(f"\n⚠️ TALHÕES CRÍTICOS (Maiores Perdas):")
        for i, (fazenda, talhao, perda_media, num_colheitas) in enumerate(criticos, 1):
            print(f"  {i}. {fazenda} - {talhao}: {perda_media}% "
                  f"({num_colheitas} colheita{'s' if num_colheitas > 1 else ''})")
    
    print("\n" + "="*70)


def gerar_relatorio_completo():
    """
    Gera relatório completo de análise
    Procedimento que exibe relatório detalhado
    """
    print("\n" + "="*70)
    print(" "*15 + "📄 RELATÓRIO COMPLETO DE ANÁLISES")
    print("="*70)
    
    if not colheitas:
        print("\nℹ️ Nenhuma colheita registrada para análise.")
        return
    
    # Dashboard
    gerar_dashboard()
    
    # Análise por variedade
    print("\n" + "="*70)
    print("🌾 ANÁLISE POR VARIEDADE:")
    print("="*70)
    
    analise_var = analisar_produtividade_por_variedade()
    
    for variedade, dados in analise_var.items():
        print(f"\n{variedade}:")
        print(f"  Colheitas: {dados['num_colheitas']}")
        print(f"  Área Total: {dados['area_total']:.2f} ha")
        print(f"  Produtividade Média: {dados['produtividade_media']:.2f} ton/ha")
        print(f"  Perda Média: {dados['perda_media']:.2f}%")
        
        if dados['produtividade_esperada']:
            print(f"  Esperado: {dados['produtividade_esperada']:.2f} ton/ha")
            print(f"  Desempenho: {dados['percentual_esperado']:.1f}% do esperado")
            
            if dados['diferenca_esperado'] > 0:
                print(f"  ✓ {dados['diferenca_esperado']:.2f} ton/ha acima do esperado")
            else:
                print(f"  ⚠️ {abs(dados['diferenca_esperado']):.2f} ton/ha abaixo do esperado")
    
    # Tabela de desempenho
    print("\n" + "="*70)
    print("📋 TABELA DE DESEMPENHO:")
    print("="*70)
    
    tabela = gerar_tabela_desempenho()
    exibir_tabela(tabela)
    
    print("\n" + "="*70)


