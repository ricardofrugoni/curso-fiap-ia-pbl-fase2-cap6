"""
Sistema de Gestão de Perdas na Colheita de Cana-de-Açúcar
Projeto: FIAP - Cap 6 - Python e Além
"""

import os
import sys
from datetime import datetime

# Importação dos módulos
from modulos import validacao, fazenda, colheita, analise, arquivo, database
from config import TIPOS_COLHEITA, TIPOS_PERDA, VARIEDADES_CANA


def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa a execução e aguarda input do usuário"""
    input("\nPressione ENTER para continuar...")


def exibir_cabecalho():
    """Exibe o cabeçalho do sistema"""
    print("=" * 70)
    print(" " * 10 + "GESTAO DE COLHEITAS DE CANA-DE-ACUCAR")
    print(" " * 15 + "Sistema de Controle de Perdas")
    print("=" * 70)


def menu_principal():
    """Exibe o menu principal e retorna a opção escolhida"""
    print("\nMENU PRINCIPAL\n")
    print("1 - Gestão de Fazendas")
    print("2 - Gestão de Talhões")
    print("3 - Registro de Colheitas")
    print("4 - Análises e Relatórios")
    print("5 - Recomendações")
    print("6 - Gerenciamento de Arquivos")
    print("7 - Banco de Dados Oracle")
    print("8 - Dados de Exemplo")
    print("0 - Sair")
    print("\n" + "-" * 70)
    
    opcao = input("Digite a opção desejada: ").strip()
    return opcao


# ==================== GESTÃO DE FAZENDAS ====================

def menu_fazendas():
    """Menu de gestão de fazendas"""
    while True:
        limpar_tela()
        exibir_cabecalho()
        
        print("\nGESTAO DE FAZENDAS\n")
        print("1 - Cadastrar nova fazenda")
        print("2 - Listar todas as fazendas")
        print("3 - Buscar fazenda por ID")
        print("4 - Buscar fazenda por nome")
        print("5 - Exibir estatísticas")
        print("0 - Voltar")
        
        opcao = input("\nOpção: ").strip()
        
        if opcao == '1':
            cadastrar_fazenda()
        elif opcao == '2':
            listar_fazendas()
        elif opcao == '3':
            buscar_fazenda_id()
        elif opcao == '4':
            buscar_fazenda_nome()
        elif opcao == '5':
            exibir_estatisticas_fazendas()
        elif opcao == '0':
            break
        else:
            print("Opcao invalida!")
            pausar()


def cadastrar_fazenda():
    """Cadastra uma nova fazenda"""
    print("\n" + "=" * 70)
    print("CADASTRO DE FAZENDA")
    print("=" * 70)
    
    arquivo.registrar_log("Iniciando cadastro de fazenda", "INFO")
    
    # Entrada de dados com validação
    nome = validacao.obter_entrada_validada('str', "Nome da fazenda: ")
    proprietario = validacao.obter_entrada_validada('str', "Nome do proprietário: ")
    
    # CPF/CNPJ com validação
    while True:
        documento = input("CPF ou CNPJ: ").strip()
        doc_limpo = documento.replace('.', '').replace('-', '').replace('/', '')
        
        if len(doc_limpo) == 11:
            if validacao.validar_cpf(documento):
                break
            print("CPF invalido! Tente novamente.")
        elif len(doc_limpo) == 14:
            if validacao.validar_cnpj(documento):
                break
            print("CNPJ invalido! Tente novamente.")
        else:
            print("Documento invalido! Use CPF (11 dígitos) ou CNPJ (14 dígitos)")
    
    localizacao = validacao.obter_entrada_validada('str', "Localização (Cidade - UF): ")
    
    # Cria a fazenda
    nova_fazenda = fazenda.criar_fazenda(nome, proprietario, documento, localizacao)
    
    if nova_fazenda:
        fazenda.adicionar_fazenda(nova_fazenda)
        arquivo.registrar_log(f"Fazenda '{nome}' cadastrada com sucesso", "INFO")
    else:
        print("Erro ao criar fazenda!")
        arquivo.registrar_log("Erro ao cadastrar fazenda", "ERRO")
    
    pausar()


def listar_fazendas():
    """Lista todas as fazendas cadastradas"""
    print("\n" + "=" * 70)
    print("LISTA DE FAZENDAS")
    print("=" * 70)
    
    lista = fazenda.listar_fazendas()
    
    if not lista:
        print("\nNenhuma fazenda cadastrada.")
    else:
        for f in lista:
            print(f"\nID: {f['id']} - {f['nome']}")
            print(f"   Proprietario: {f['proprietario']}")
            print(f"   {f['tipo_documento']}: {f['documento']}")
            print(f"   Localizacao: {f['localizacao']}")
            print(f"   Area Total: {f['area_total']:.2f} ha")
            print(f"   Talhoes: {len(f['talhoes'])}")
    
    print(f"\nTotal: {len(lista)} fazenda(s)")
    pausar()


def buscar_fazenda_id():
    """Busca uma fazenda por ID"""
    print("\n" + "=" * 70)
    print("BUSCAR FAZENDA POR ID")
    print("=" * 70)
    
    id_fazenda = validacao.obter_entrada_validada('int', "ID da fazenda: ")
    
    f = fazenda.buscar_fazenda_por_id(id_fazenda)
    
    if f:
        fazenda.exibir_fazenda_detalhada(f)
    else
        print(f"\nFazenda com ID {id_fazenda} nao encontrada!")
    
    pausar()


def buscar_fazenda_nome():
    """Busca fazendas por nome"""
    print("\n" + "=" * 70)
    print("BUSCAR FAZENDA POR NOME")
    print("=" * 70)
    
    nome = input("Nome (ou parte do nome): ").strip()
    
    encontradas = fazenda.buscar_fazenda_por_nome(nome)
    
    if not encontradas:
        print(f"\nNenhuma fazenda encontrada com '{nome}'")
    else:
        print(f"\n{len(encontradas)} fazenda(s) encontrada(s):\n")
        for f in encontradas:
            print(f"  ID {f['id']}: {f['nome']} - {f['localizacao']}")
    
    pausar()


def exibir_estatisticas_fazendas():
    """Exibe estatísticas das fazendas"""
    print("\n" + "=" * 70)
    print("ESTATÍSTICAS DE FAZENDAS")
    print("=" * 70)
    
    stats = fazenda.obter_estatisticas_fazendas()
    
    print(f"\nResumo Geral:")
    print(f"  Total de Fazendas: {stats['total_fazendas']}")
    print(f"  Total de Talhoes: {stats['total_talhoes']}")
    print(f"  Area Total: {stats['area_total']:.2f} hectares")
    print(f"  Media de Area por Fazenda: {stats['media_area_fazenda']:.2f} ha")
    
    if stats['variedades']:
        print(f"\nDistribuicao por Variedade:")
        for variedade, area in sorted(stats['variedades'].items(), key=lambda x: x[1], reverse=True):
            percentual = (area / stats['area_total'] * 100) if stats['area_total'] > 0 else 0
            print(f"  {variedade}: {area:.2f} ha ({percentual:.1f}%)")
    
    pausar()


# ==================== GESTÃO DE TALHÕES ====================

def menu_talhoes():
    """Menu de gestão de talhões"""
    while True:
        limpar_tela()
        exibir_cabecalho()
        
        print("\nGESTAO DE TALHOES\n")
        print("1 - Adicionar talhao a uma fazenda")
        print("2 - Buscar talhao")
        print("3 - Listar talhoes de uma fazenda")
        print("0 - Voltar")
        
        opcao = input("\nOpcao: ").strip()
        
        if opcao == '1':
            adicionar_talhao()
        elif opcao == '2':
            buscar_talhao()
        elif opcao == '3':
            listar_talhoes_fazenda()
        elif opcao == '0':
            break
        else:
            print("Opcao invalida!")
            pausar()


def adicionar_talhao():
    """Adiciona um talhão a uma fazenda"""
    print("\n" + "=" * 70)
    print("ADICIONAR TALHÃO")
    print("=" * 70)
    
    # Lista fazendas disponíveis
    lista = fazenda.listar_fazendas()
    if not lista
        print("\nNenhuma fazenda cadastrada! Cadastre uma fazenda primeiro.")
        pausar()
        return
    
    print("\nFazendas disponiveis:")
    for f in lista:
        print(f"  ID {f['id']}: {f['nome']}")
    
    id_fazenda = validacao.obter_entrada_validada('int', "\nID da fazenda: ")
    
    # Verifica se a fazenda existe
    f = fazenda.buscar_fazenda_por_id(id_fazenda)
    if not f:
        print(f"\nFazenda com ID {id_fazenda} nao encontrada!")
        pausar()
        return
    
    print(f"\nFazenda selecionada: {f['nome']}")
    
    # Dados do talhão
    codigo = input("\nCódigo do talhão (ex: T01): ").strip().upper()
    area = validacao.obter_entrada_validada('float', "Área (hectares): ", validacao.validar_area)
    
    print(f"\nVariedades disponíveis: {', '.join(VARIEDADES_CANA)}")
    variedade = validacao.obter_entrada_validada('str', "Variedade: ", validacao.validar_variedade)
    
    ano_atual = datetime.now().year
    ano_plantio = validacao.obter_entrada_validada('int', f"Ano do plantio (ex: {ano_atual}): ",
                                                   lambda x: 1900 <= x <= ano_atual)
    
    # Cria e adiciona o talhão
    novo_talhao = fazenda.criar_talhao(codigo, area, variedade, ano_plantio)
    
    if novo_talhao:
        fazenda.adicionar_talhao_fazenda(id_fazenda, novo_talhao)
        arquivo.registrar_log(f"Talhão '{codigo}' adicionado à fazenda ID {id_fazenda}", "INFO")
    else:
        print("Erro ao criar talhao!")
        arquivo.registrar_log("Erro ao adicionar talhão", "ERRO")
    
    pausar()


def buscar_talhao():
    """Busca um talhão específico"""
    print("\n" + "=" * 70)
    print("BUSCAR TALHÃO")
    print("=" * 70)
    
    id_fazenda = validacao.obter_entrada_validada('int', "ID da fazenda: ")
    codigo = input("Código do talhão: ").strip()
    
    f, t = fazenda.buscar_talhao(id_fazenda, codigo)
    
    if not f:
        print(f"\nFazenda com ID {id_fazenda} nao encontrada!")
    elif not t:
        print(f"\nTalhao '{codigo}' nao encontrado na fazenda!")
    else:
        print(f"\nTalhao Encontrado:")
        print(f"\n  Fazenda: {f['nome']}")
        print(f"  Codigo: {t['codigo']}")
        print(f"  Area: {t['area']} hectares")
        print(f"  Variedade: {t['variedade']}")
        print(f"  Plantio: {t['ano_plantio']} ({t['idade_anos']} anos)")
        print(f"  Status: {t['status']}")
    
    pausar()


def listar_talhoes_fazenda():
    """Lista todos os talhões de uma fazenda"""
    print("\n" + "=" * 70)
    print("TALHÕES DE UMA FAZENDA")
    print("=" * 70)
    
    id_fazenda = validacao.obter_entrada_validada('int', "ID da fazenda: ")
    
    f = fazenda.buscar_fazenda_por_id(id_fazenda)
    
    if not f:
        print(f"\nFazenda com ID {id_fazenda} nao encontrada!")
    elif not f['talhoes']:
        print(f"\nA fazenda '{f['nome']}' nao possui talhoes cadastrados.")
    else:
        print(f"\nTalhoes da Fazenda: {f['nome']}")
        print("-" * 70)
        
        for t in f['talhoes']:
            print(f"\n  Codigo: {t['codigo']}")
            print(f"  Area: {t['area']} ha")
            print(f"  Variedade: {t['variedade']}")
            print(f"  Plantio: {t['ano_plantio']} ({t['idade_anos']} anos)")
        
        print(f"\nTotal: {len(f['talhoes'])} talhao/oes - Area total: {f['area_total']:.2f} ha")
    
    pausar()


# ==================== REGISTRO DE COLHEITAS ====================

def menu_colheitas():
    """Menu de registro de colheitas"""
    while True:
        limpar_tela()
        exibir_cabecalho()
        
        print("\nREGISTRO DE COLHEITAS\n")
        print("1 - Registrar nova colheita")
        print("2 - Listar todas as colheitas")
        print("3 - Buscar colheita por ID")
        print("4 - Colheitas de uma fazenda")
        print("5 - Colheitas de um talhao")
        print("6 - Estatisticas de colheitas")
        print("0 - Voltar")
        
        opcao = input("\nOpcao: ").strip()
        
        if opcao == '1':
            registrar_colheita()
        elif opcao == '2':
            listar_colheitas()
        elif opcao == '3':
            buscar_colheita_id()
        elif opcao == '4':
            listar_colheitas_fazenda()
        elif opcao == '5':
            listar_colheitas_talhao()
        elif opcao == '6':
            exibir_estatisticas_colheitas()
        elif opcao == '0':
            break
        else:
            print("Opcao invalida!")
            pausar()


def registrar_colheita():
    """Registra uma nova colheita"""
    print("\n" + "=" * 70)
    print("REGISTRAR COLHEITA")
    print("=" * 70)
    
    arquivo.registrar_log("Iniciando registro de colheita", "INFO")
    
    # Lista fazendas disponíveis
    lista = fazenda.listar_fazendas()
    if not lista:
        print("\nNenhuma fazenda cadastrada!")
        pausar()
        return
    
    print("\nFazendas disponiveis:")
    for f in lista:
        print(f"  ID {f['id']}: {f['nome']}")
    
    id_fazenda = validacao.obter_entrada_validada('int', "\nID da fazenda: ")
    
    f = fazenda.buscar_fazenda_por_id(id_fazenda)
    if not f:
        print(f"\nFazenda nao encontrada!")
        pausar()
        return
    
    if not f['talhoes']:
        print(f"\nA fazenda '{f['nome']}' nao possui talhoes cadastrados!")
        pausar()
        return
    
    print(f"\nFazenda: {f['nome']}")
    print("\nTalhoes disponiveis:")
    for t in f['talhoes']:
        print(f"  {t['codigo']}: {t['area']} ha - {t['variedade']}")
    
    codigo_talhao = input("\nCódigo do talhão: ").strip()
    
    _, talhao = fazenda.buscar_talhao(id_fazenda, codigo_talhao)
    if not talhao:
        print(f"\nTalhao '{codigo_talhao}' nao encontrado!")
        pausar()
        return
    
    # Dados da colheita
    print(f"\nTalhao: {codigo_talhao} - Area: {talhao['area']} ha")
    
    while True:
        data_colheita = input("\nData da colheita (DD/MM/AAAA): ").strip()
        if validacao.validar_data(data_colheita):
            break
    
    print(f"\nTipos de colheita: {', '.join(TIPOS_COLHEITA)}")
    tipo = validacao.obter_entrada_validada('str', "Tipo de colheita: ", 
                                            validacao.validar_tipo_colheita)
    
    quantidade = validacao.obter_entrada_validada('float', 
                                                  f"Quantidade colhida (toneladas): ")
    
    # Registro de perdas
    print(f"\nREGISTRO DE PERDAS")
    print(f"Tipos disponiveis: {', '.join(TIPOS_PERDA)}")
    print("Digite o percentual para cada tipo (0 se nao houver perda)\n")
    
    perdas_dict = {}
    for tipo_perda in TIPOS_PERDA:
        while True:
            valor = validacao.validar_float(
                input(f"  {tipo_perda.capitalize()} (%): ").strip()
            )
            if valor is not None and validacao.validar_perda(valor):
                if valor > 0:  # Só adiciona se houver perda
                    perdas_dict[tipo_perda] = valor
                break
    
    if not perdas_dict:
        print("\nNenhuma perda registrada. Adicionando perda minima de 0.1%")
        perdas_dict['mecânica'] = 0.1
    
    # Cria a colheita
    nova_colheita = colheita.criar_colheita(
        id_fazenda, codigo_talhao, data_colheita, tipo, quantidade, perdas_dict
    )
    
    if nova_colheita:
        colheita.adicionar_colheita(nova_colheita)
        arquivo.registrar_log(
            f"Colheita registrada: Fazenda {id_fazenda}, Talhão {codigo_talhao}", "INFO"
        )
    else:
        print("Erro ao registrar colheita!")
        arquivo.registrar_log("Erro ao registrar colheita", "ERRO")
    
    pausar()


def listar_colheitas():
    """Lista todas as colheitas"""
    print("\n" + "=" * 70)
    print("LISTA DE COLHEITAS")
    print("=" * 70)
    
    lista = colheita.listar_colheitas()
    
    if not lista:
        print("\nNenhuma colheita registrada.")
    else:
        for c in lista:
            print(f"\nID: {c['id']} - {c['nome_fazenda']}")
            print(f"   Talhao: {c['codigo_talhao']} | Data: {c['data_colheita']}")
            print(f"   Tipo: {c['tipo_colheita'].upper()} | Variedade: {c['variedade']}")
            print(f"   Producao: {c['quantidade_colhida']:.2f} t | "
                  f"Produtividade: {c['produtividade']:.2f} t/ha")
            print(f"   Perda: {c['percentual_perda_total']:.2f}% | Status: {c['status']}")
    
    print(f"\nTotal: {len(lista)} colheita(s)")
    pausar()


def buscar_colheita_id():
    """Busca uma colheita por ID"""
    print("\n" + "=" * 70)
    print("BUSCAR COLHEITA POR ID")
    print("=" * 70)
    
    id_colheita = validacao.obter_entrada_validada('int', "ID da colheita: ")
    
    c = colheita.buscar_colheita_por_id(id_colheita)
    
    if c:
        colheita.exibir_colheita_detalhada(c)
    else:
        print(f"\nColheita com ID {id_colheita} nao encontrada!")
    
    pausar()


def listar_colheitas_fazenda():
    """Lista colheitas de uma fazenda"""
    print("\n" + "=" * 70)
    print("COLHEITAS DE UMA FAZENDA")
    print("=" * 70)
    
    id_fazenda = validacao.obter_entrada_validada('int', "ID da fazenda: ")
    
    lista = colheita.buscar_colheitas_fazenda(id_fazenda)
    
    if not lista:
        print(f"\nNenhuma colheita registrada para a fazenda ID {id_fazenda}")
    else:
        f = fazenda.buscar_fazenda_por_id(id_fazenda)
        print(f"\nColheitas da Fazenda: {f['nome'] if f else 'N/A'}")
        print("-" * 70)
        
        for c in lista:
            print(f"\n  ID {c['id']}: {c['codigo_talhao']} - {c['data_colheita']}")
            print(f"  Producao: {c['quantidade_colhida']:.2f} t | Perda: {c['percentual_perda_total']:.2f}%")
        
        print(f"\nTotal: {len(lista)} colheita(s)")
    
    pausar()


def listar_colheitas_talhao():
    """Lista colheitas de um talhão"""
    print("\n" + "=" * 70)
    print("COLHEITAS DE UM TALHÃO")
    print("=" * 70)
    
    id_fazenda = validacao.obter_entrada_validada('int', "ID da fazenda: ")
    codigo = input("Código do talhão: ").strip()
    
    lista = colheita.buscar_colheitas_talhao(id_fazenda, codigo)
    
    if not lista:
        print(f"\nNenhuma colheita registrada para o talhao '{codigo}'")
    else:
        print(f"\nColheitas do Talhao: {codigo}")
        print("-" * 70)
        
        for c in lista:
            print(f"\n  ID {c['id']}: {c['data_colheita']} - {c['tipo_colheita'].upper()}")
            print(f"  Produtividade: {c['produtividade']:.2f} t/ha | Perda: {c['percentual_perda_total']:.2f}%")
        
        print(f"\nTotal: {len(lista)} colheita(s)")
    
    pausar()


def exibir_estatisticas_colheitas():
    """Exibe estatísticas das colheitas"""
    print("\n" + "=" * 70)
    print("ESTATÍSTICAS DE COLHEITAS")
    print("=" * 70)
    
    stats = colheita.obter_estatisticas_colheitas()
    
    if stats['total_colheitas'] == 0:
        print("\nNenhuma colheita registrada para analise.")
    else:
        print(f"\nResumo Geral:")
        print(f"  Total de Colheitas: {stats['total_colheitas']}")
        print(f"  Area Total Colhida: {stats['area_total_colhida']} ha")
        print(f"  Producao Total: {stats['producao_total']} toneladas")
        print(f"  Perda Total: {stats['perda_total']} toneladas")
        print(f"  Produtividade Media: {stats['produtividade_media']} ton/ha")
        print(f"  Perda Media: {stats['perda_media']}%")
        
        if 'por_tipo' in stats and stats['por_tipo']:
            print(f"\nPor Tipo de Colheita:")
            for tipo, dados in stats['por_tipo'].items():
                print(f"\n  {tipo.upper()}:")
                print(f"    Quantidade: {dados['quantidade']}")
                print(f"    Produtividade Media: {dados['produtividade_media']:.2f} ton/ha")
                print(f"    Perda Media: {dados['perda_media']:.2f}%")
    
    pausar()


# ==================== ANÁLISES E RELATÓRIOS ====================

def menu_analises():
    """Menu de análises e relatórios"""
    while True:
        limpar_tela()
        exibir_cabecalho()
        
        print("\nANALISES E RELATORIOS\n")
        print("1 - Dashboard Geral")
        print("2 - Relatorio Completo")
        print("3 - Tabela de Desempenho")
        print("4 - Analise por Variedade")
        print("5 - Comparar Metodos de Colheita")
        print("6 - Identificar Talhoes Criticos")
        print("0 - Voltar")
        
        opcao = input("\nOpcao: ").strip()
        
        if opcao == '1':
            limpar_tela()
            exibir_cabecalho()
            analise.gerar_dashboard()
            pausar()
        elif opcao == '2':
            limpar_tela()
            exibir_cabecalho()
            analise.gerar_relatorio_completo()
            pausar()
        elif opcao == '3':
            exibir_tabela_desempenho()
        elif opcao == '4':
            exibir_analise_variedade()
        elif opcao == '5':
            comparar_metodos()
        elif opcao == '6':
            exibir_talhoes_criticos()
        elif opcao == '0':
            break
        else:
            print("Opcao invalida!")
            pausar()


def exibir_tabela_desempenho():
    """Exibe tabela de desempenho"""
    limpar_tela()
    exibir_cabecalho()
    
    tabela = analise.gerar_tabela_desempenho()
    analise.exibir_tabela(tabela)
    pausar()


def exibir_analise_variedade():
    """Exibe análise por variedade"""
    print("\n" + "=" * 70)
    print("ANÁLISE POR VARIEDADE")
    print("=" * 70)
    
    analise_var = analise.analisar_produtividade_por_variedade()
    
    if not analise_var:
        print("\nNenhum dado disponivel para analise.")
    else:
        for variedade, dados in analise_var.items():
            print(f"\n{variedade}:")
            print(f"  Colheitas: {dados['num_colheitas']}")
            print(f"  Area Total: {dados['area_total']:.2f} ha")
            print(f"  Produtividade Media: {dados['produtividade_media']:.2f} ton/ha")
            print(f"  Perda Media: {dados['perda_media']:.2f}%")
            
            if dados['produtividade_esperada']:
                print(f"  Esperado: {dados['produtividade_esperada']:.2f} ton/ha")
                print(f"  Desempenho: {dados['percentual_esperado']:.1f}% do esperado")
    
    pausar()


def comparar_metodos():
    """Compara métodos de colheita"""
    print("\n" + "=" * 70)
    print("COMPARAÇÃO DE MÉTODOS DE COLHEITA")
    print("=" * 70)
    
    comparacao = colheita.comparar_metodos_colheita()
    
    print(f"\nManual:")
    print(f"  Colheitas: {comparacao['manual']['quantidade']}")
    print(f"  Perda Media: {comparacao['manual']['perda_media']}%")
    
    print(f"\nMecanica:")
    print(f"  Colheitas: {comparacao['mecanica']['quantidade']}")
    print(f"  Perda Media: {comparacao['mecanica']['perda_media']}%")
    
    print(f"\nDiferenca: {abs(comparacao['diferenca'])}% ")
    if comparacao['diferenca'] > 0:
        print("   (Mecanica tem perdas maiores)")
    elif comparacao['diferenca'] < 0:
        print("   (Manual tem perdas maiores)")
    else:
        print("   (Sem diferenca significativa)")
    
    pausar()


def exibir_talhoes_criticos():
    """Exibe talhões críticos"""
    print("\n" + "=" * 70)
    print("TALHÕES CRÍTICOS (Maiores Perdas)")
    print("=" * 70)
    
    criticos = analise.identificar_talhoes_criticos()
    
    if not criticos:
        print("\nNenhum dado disponivel.")
    else:
        print(f"\nTop 10 Talhoes com Maiores Perdas:\n")
        for i, (fazenda, talhao, perda, num_colh) in enumerate(criticos[:10], 1):
            print(f"  {i}. {fazenda} - {talhao}")
            print(f"     Perda Media: {perda}% ({num_colh} colheita(s))")
    
    pausar()


# ==================== RECOMENDAÇÕES ====================

def menu_recomendacoes():
    """Menu de recomendações"""
    limpar_tela()
    exibir_cabecalho()
    
    print("\nRECOMENDACOES\n")
    
    lista = colheita.listar_colheitas()
    
    if not lista:
        print("Nenhuma colheita registrada para analise.")
        pausar()
        return
    
    print("Colheitas disponiveis:")
    for c in lista[:10]:  # Mostra as 10 mais recentes
        print(f"  ID {c['id']}: {c['nome_fazenda']} - {c['codigo_talhao']} "
              f"(Perda: {c['percentual_perda_total']:.1f}%)")
    
    id_colheita = validacao.obter_entrada_validada('int', "\nID da colheita para analise: ")
    
    c = colheita.buscar_colheita_por_id(id_colheita)
    
    if not c:
        print(f"\nColheita nao encontrada!")
    else:
        print("\n" + "=" * 70)
        print(f"RECOMENDACOES - Colheita #{c['id']}")
        print("=" * 70)
        
        print(f"\nFazenda: {c['nome_fazenda']}")
        print(f"Talhao: {c['codigo_talhao']}")
        print(f"Perda Total: {c['percentual_perda_total']:.2f}%")
        print(f"Status: {c['status']}")
        
        recomendacoes = analise.gerar_recomendacoes(c)
        
        print(f"\nRECOMENDACOES:\n")
        for i, rec in enumerate(recomendacoes, 1):
            print(f"  {i}. {rec}")
    
    pausar()


# ==================== GERENCIAMENTO DE ARQUIVOS ====================

def menu_arquivos():
    """Menu de gerenciamento de arquivos"""
    while True:
        limpar_tela()
        exibir_cabecalho()
        
        print("\nGERENCIAMENTO DE ARQUIVOS\n")
        print("1 - Salvar dados em JSON")
        print("2 - Carregar dados de JSON")
        print("3 - Exportar relatorio em texto")
        print("4 - Visualizar logs")
        print("5 - Status dos arquivos")
        print("6 - Criar backup")
        print("0 - Voltar")
        
        opcao = input("\nOpcao: ").strip()
        
        if opcao == '1':
            salvar_json()
        elif opcao == '2':
            carregar_json()
        elif opcao == '3':
            exportar_relatorio()
        elif opcao == '4':
            visualizar_logs()
        elif opcao == '5':
            arquivo.exibir_status_arquivos()
            pausar()
        elif opcao == '6':
            arquivo.backup_dados()
            pausar()
        elif opcao == '0':
            break
        else:
            print("Opcao invalida!")
            pausar()


def salvar_json():
    """Salva dados em JSON"""
    print("\nSalvando dados...")
    
    sucesso_f = arquivo.salvar_fazendas_json(fazenda.listar_fazendas())
    sucesso_c = arquivo.salvar_colheitas_json(colheita.listar_colheitas())
    
    if sucesso_f and sucesso_c:
        print("Dados salvos com sucesso!")
    else:
        print("Houve erros ao salvar alguns dados.")
    
    pausar()


def carregar_json():
    """Carrega dados de JSON"""
    print("\nCarregando dados...")
    
    fazendas_carregadas = arquivo.carregar_fazendas_json()
    colheitas_carregadas = arquivo.carregar_colheitas_json()
    
    if fazendas_carregadas:
        fazenda.fazendas.clear()
        fazenda.fazendas.extend(fazendas_carregadas)
        print(f"{len(fazendas_carregadas)} fazenda(s) carregada(s)")
    
    if colheitas_carregadas:
        colheita.colheitas.clear()
        colheita.colheitas.extend(colheitas_carregadas)
        print(f"{len(colheitas_carregadas)} colheita(s) carregada(s)")
    
    if not fazendas_carregadas and not colheitas_carregadas:
        print("Nenhum dado encontrado para carregar.")
    
    pausar()


def exportar_relatorio():
    """Exporta relatório em texto"""
    print("\nExportar Relatorio\n")
    print("1 - Dashboard")
    print("2 - Relatorio Completo")
    print("3 - Lista de Fazendas")
    print("4 - Lista de Colheitas")
    
    opcao = input("\nOpcao: ").strip()
    
    # Captura a saída em string (simplificado - apenas exemplo)
    if opcao in ['1', '2', '3', '4']:
        conteudo = "Relatorio gerado em " + datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        conteudo += "\n\nConteudo do relatorio aqui..."
        
        arquivo.exportar_relatorio_texto("relatorio", conteudo)
    else:
        print("Opcao invalida!")
    
    pausar()


def visualizar_logs():
    """Visualiza os logs"""
    limpar_tela()
    exibir_cabecalho()
    
    num = validacao.obter_entrada_validada('int', "Número de linhas (padrão 20): ")
    arquivo.exibir_logs(num if num else 20)
    
    pausar()


# ==================== BANCO DE DADOS ====================

def menu_banco_dados():
    """Menu de banco de dados"""
    while True:
        limpar_tela()
        exibir_cabecalho()
        
        print("\nBANCO DE DADOS ORACLE\n")
        print("1 - Testar conexao")
        print("2 - Criar tabelas")
        print("3 - Sincronizar dados (Memoria -> BD)")
        print("4 - Carregar dados (BD -> Memoria)")
        print("0 - Voltar")
        
        opcao = input("\nOpcao: ").strip()
        
        if opcao == '1':
            print("\nTestando conexao...")
            database.testar_conexao()
            pausar()
        elif opcao == '2':
            print("\nCriando tabelas...")
            database.criar_tabelas()
            pausar()
        elif opcao == '3':
            sincronizar_bd()
        elif opcao == '4':
            carregar_bd()
        elif opcao == '0':
            break
        else:
            print("Opcao invalida!")
            pausar()


def sincronizar_bd():
    """Sincroniza dados com o banco"""
    print("\nSincronizando dados com o banco...")
    
    confirmacao = input("Isso substituira todos os dados do BD. Confirma? (S/N): ").strip().upper()
    
    if confirmacao == 'S':
        sucesso = database.sincronizar_dados_bd(
            fazenda.listar_fazendas(),
            colheita.listar_colheitas()
        )
        
        if sucesso:
            print("\nSincronizacao concluida!")
        else:
            print("\nHouve erros na sincronizacao.")
    else:
        print("\nSincronizacao cancelada.")
    
    pausar()


def carregar_bd():
    """Carrega dados do banco"""
    print("\nCarregando dados do banco...")
    
    confirmacao = input("Isso substituira os dados em memoria. Confirma? (S/N): ").strip().upper()
    
    if confirmacao == 'S':
        fazendas_bd = database.buscar_fazendas()
        colheitas_bd = database.buscar_colheitas()
        
        if fazendas_bd:
            fazenda.fazendas.clear()
            fazenda.fazendas.extend(fazendas_bd)
            print(f"{len(fazendas_bd)} fazenda(s) carregada(s)")
        
        if colheitas_bd:
            colheita.colheitas.clear()
            colheita.colheitas.extend(colheitas_bd)
            print(f"{len(colheitas_bd)} colheita(s) carregada(s)")
        
        if not fazendas_bd and not colheitas_bd:
            print("Nenhum dado encontrado no banco.")
    else:
        print("\nOperacao cancelada.")
    
    pausar()


# ==================== DADOS DE EXEMPLO ====================

def carregar_dados_exemplo():
    """Carrega dados de exemplo para demonstração"""
    print("\nCarregando dados de exemplo...")
    
    arquivo.registrar_log("Carregando dados de exemplo", "INFO")
    
    # Limpa dados existentes
    fazenda.fazendas.clear()
    colheita.colheitas.clear()
    
    # Fazenda 1
    f1 = fazenda.criar_fazenda(
        "Fazenda Santa Rita",
        "João Silva",
        "123.456.789-00",
        "Ribeirão Preto - SP",
        0
    )
    fazenda.adicionar_fazenda(f1)
    
    t1 = fazenda.criar_talhao("T01", 15.5, "RB867515", 2020)
    fazenda.adicionar_talhao_fazenda(f1['id'], t1)
    
    t2 = fazenda.criar_talhao("T02", 12.0, "CTC4", 2021)
    fazenda.adicionar_talhao_fazenda(f1['id'], t2)
    
    # Fazenda 2
    f2 = fazenda.criar_fazenda(
        "Agro Paulista",
        "Maria Santos",
        "98.765.432-10",
        "Sertãozinho - SP",
        0
    )
    fazenda.adicionar_fazenda(f2)
    
    t3 = fazenda.criar_talhao("A01", 20.0, "RB966928", 2019)
    fazenda.adicionar_talhao_fazenda(f2['id'], t3)
    
    t4 = fazenda.criar_talhao("A02", 18.5, "CTC20", 2020)
    fazenda.adicionar_talhao_fazenda(f2['id'], t4)
    
    # Fazenda 3
    f3 = fazenda.criar_fazenda(
        "Usina Verde",
        "Carlos Oliveira",
        "12.345.678/0001-90",
        "Piracicaba - SP",
        0
    )
    fazenda.adicionar_fazenda(f3)
    
    t5 = fazenda.criar_talhao("U01", 25.0, "SP813250", 2018)
    fazenda.adicionar_talhao_fazenda(f3['id'], t5)
    
    # Colheitas
    c1 = colheita.criar_colheita(
        f1['id'], "T01", "15/09/2024", "mecânica", 1240.0,
        {'mecânica': 12.0, 'raizame': 2.5, 'palha': 1.8}
    )
    colheita.adicionar_colheita(c1)
    
    c2 = colheita.criar_colheita(
        f1['id'], "T02", "18/09/2024", "manual", 1050.0,
        {'mecânica': 3.5, 'raizame': 1.2}
    )
    colheita.adicionar_colheita(c2)
    
    c3 = colheita.criar_colheita(
        f2['id'], "A01", "20/09/2024", "mecânica", 1680.0,
        {'mecânica': 14.5, 'palha': 2.3, 'climática': 1.0}
    )
    colheita.adicionar_colheita(c3)
    
    c4 = colheita.criar_colheita(
        f2['id'], "A02", "22/09/2024", "mecânica", 1590.0,
        {'mecânica': 11.0, 'raizame': 2.0}
    )
    colheita.adicionar_colheita(c4)
    
    c5 = colheita.criar_colheita(
        f3['id'], "U01", "25/09/2024", "manual", 1950.0,
        {'mecânica': 4.2, 'raizame': 1.5}
    )
    colheita.adicionar_colheita(c5)
    
    print("Dados de exemplo carregados com sucesso!")
    print(f"  {len(fazenda.fazendas)} fazendas")
    print(f"  {sum(len(f['talhoes']) for f in fazenda.fazendas)} talhoes")
    print(f"  {len(colheita.colheitas)} colheitas")
    
    arquivo.registrar_log("Dados de exemplo carregados", "INFO")
    pausar()


# ==================== MAIN ====================

def main():
    """Função principal do sistema"""
    # Registra início
    arquivo.registrar_log("Sistema iniciado", "INFO")
    
    # Tenta carregar dados existentes
    fazendas_carregadas = arquivo.carregar_fazendas_json()
    if fazendas_carregadas:
        fazenda.fazendas.extend(fazendas_carregadas)
    
    colheitas_carregadas = arquivo.carregar_colheitas_json()
    if colheitas_carregadas:
        colheita.colheitas.extend(colheitas_carregadas)
    
    # Loop principal
    while True:
        limpar_tela()
        exibir_cabecalho()
        
        opcao = menu_principal()
        
        if opcao == '1':
            menu_fazendas()
        elif opcao == '2':
            menu_talhoes()
        elif opcao == '3':
            menu_colheitas()
        elif opcao == '4':
            menu_analises()
        elif opcao == '5':
            menu_recomendacoes()
        elif opcao == '6':
            menu_arquivos()
        elif opcao == '7':
            menu_banco_dados()
        elif opcao == '8':
            carregar_dados_exemplo()
        elif opcao == '0':
            print("\n" + "=" * 70)
            print("Salvando dados antes de sair...")
            arquivo.salvar_fazendas_json(fazenda.listar_fazendas())
            arquivo.salvar_colheitas_json(colheita.listar_colheitas())
            print("Dados salvos!")
            arquivo.registrar_log("Sistema encerrado", "INFO")
            print("\nObrigado por usar o sistema!")
            print("=" * 70)
            break
        else:
            print("\nOpcao invalida!")
            pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSistema interrompido pelo usuario.")
        arquivo.registrar_log("Sistema interrompido pelo usuario", "AVISO")
    except Exception as e:
        print(f"\n\nErro fatal: {e}")
        arquivo.registrar_log(f"Erro fatal: {e}", "ERRO")
        sys.exit(1)


