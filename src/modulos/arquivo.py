"""
Módulo de manipulação de arquivos
Capítulo 5: Arquivos texto e JSON
"""

import json
import os
from datetime import datetime
from config import ARQUIVO_FAZENDAS, ARQUIVO_COLHEITAS, ARQUIVO_LOGS


def registrar_log(mensagem, tipo="INFO"):
    """
    Registra uma mensagem no arquivo de log
    Manipulação de arquivo texto com append
    
    Parâmetros:
        mensagem (str): mensagem a ser registrada
        tipo (str): tipo de log (INFO, ERRO, AVISO)
    """
    try:
        # Cria diretório se não existir
        os.makedirs(os.path.dirname(ARQUIVO_LOGS), exist_ok=True)
        
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        linha_log = f"[{timestamp}] [{tipo}] {mensagem}\n"
        
        # Abre arquivo em modo append
        with open(ARQUIVO_LOGS, 'a', encoding='utf-8') as arquivo:
            arquivo.write(linha_log)
        
        return True
    except Exception as e:
        print(f"✗ Erro ao registrar log: {e}")
        return False


def ler_logs(num_linhas=50):
    """
    Lê as últimas N linhas do arquivo de log
    Leitura de arquivo texto
    
    Parâmetro:
        num_linhas (int): número de linhas a ler
    
    Retorna:
        list: lista com as últimas linhas do log
    """
    try:
        if not os.path.exists(ARQUIVO_LOGS):
            return []
        
        with open(ARQUIVO_LOGS, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        
        # Retorna as últimas N linhas
        return linhas[-num_linhas:]
    except Exception as e:
        print(f"✗ Erro ao ler logs: {e}")
        return []


def exibir_logs(num_linhas=20):
    """
    Exibe os logs mais recentes
    Procedimento que lê e exibe arquivo texto
    
    Parâmetro:
        num_linhas (int): número de linhas a exibir
    """
    print("\n" + "="*70)
    print(f"📋 ÚLTIMOS {num_linhas} REGISTROS DE LOG")
    print("="*70)
    
    linhas = ler_logs(num_linhas)
    
    if not linhas:
        print("\nNenhum log encontrado.")
    else:
        for linha in linhas:
            print(linha.strip())
    
    print("="*70)


def salvar_fazendas_json(lista_fazendas):
    """
    Salva lista de fazendas em arquivo JSON
    Escrita de arquivo JSON
    
    Parâmetro:
        lista_fazendas (list): lista de fazendas a salvar
    
    Retorna:
        bool: True se salvo com sucesso
    """
    try:
        # Cria diretório se não existir
        os.makedirs(os.path.dirname(ARQUIVO_FAZENDAS), exist_ok=True)
        
        # Converte para JSON e salva
        with open(ARQUIVO_FAZENDAS, 'w', encoding='utf-8') as arquivo:
            json.dump(lista_fazendas, arquivo, ensure_ascii=False, indent=2)
        
        registrar_log(f"Fazendas salvas em JSON: {len(lista_fazendas)} registros", "INFO")
        return True
    except Exception as e:
        print(f"✗ Erro ao salvar fazendas: {e}")
        registrar_log(f"Erro ao salvar fazendas: {e}", "ERRO")
        return False


def carregar_fazendas_json():
    """
    Carrega lista de fazendas do arquivo JSON
    Leitura de arquivo JSON
    
    Retorna:
        list: lista de fazendas ou lista vazia
    """
    try:
        if not os.path.exists(ARQUIVO_FAZENDAS):
            return []
        
        with open(ARQUIVO_FAZENDAS, 'r', encoding='utf-8') as arquivo:
            fazendas = json.load(arquivo)
        
        registrar_log(f"Fazendas carregadas do JSON: {len(fazendas)} registros", "INFO")
        return fazendas
    except json.JSONDecodeError as e:
        print(f"✗ Erro ao decodificar JSON de fazendas: {e}")
        registrar_log(f"Erro ao decodificar JSON de fazendas: {e}", "ERRO")
        return []
    except Exception as e:
        print(f"✗ Erro ao carregar fazendas: {e}")
        registrar_log(f"Erro ao carregar fazendas: {e}", "ERRO")
        return []


def salvar_colheitas_json(lista_colheitas):
    """
    Salva lista de colheitas em arquivo JSON
    Escrita de arquivo JSON com estrutura complexa
    
    Parâmetro:
        lista_colheitas (list): lista de colheitas a salvar
    
    Retorna:
        bool: True se salvo com sucesso
    """
    try:
        # Cria diretório se não existir
        os.makedirs(os.path.dirname(ARQUIVO_COLHEITAS), exist_ok=True)
        
        # Converte tuplas para listas (JSON não suporta tuplas)
        colheitas_serializaveis = []
        for colheita in lista_colheitas:
            colheita_copia = colheita.copy()
            # Converte tupla resumo_perdas para lista
            if 'resumo_perdas' in colheita_copia:
                colheita_copia['resumo_perdas'] = list(colheita_copia['resumo_perdas'])
            colheitas_serializaveis.append(colheita_copia)
        
        # Salva em JSON
        with open(ARQUIVO_COLHEITAS, 'w', encoding='utf-8') as arquivo:
            json.dump(colheitas_serializaveis, arquivo, ensure_ascii=False, indent=2)
        
        registrar_log(f"Colheitas salvas em JSON: {len(lista_colheitas)} registros", "INFO")
        return True
    except Exception as e:
        print(f"✗ Erro ao salvar colheitas: {e}")
        registrar_log(f"Erro ao salvar colheitas: {e}", "ERRO")
        return False


def carregar_colheitas_json():
    """
    Carrega lista de colheitas do arquivo JSON
    Leitura de arquivo JSON
    
    Retorna:
        list: lista de colheitas ou lista vazia
    """
    try:
        if not os.path.exists(ARQUIVO_COLHEITAS):
            return []
        
        with open(ARQUIVO_COLHEITAS, 'r', encoding='utf-8') as arquivo:
            colheitas = json.load(arquivo)
        
        # Converte listas de volta para tuplas onde necessário
        for colheita in colheitas:
            if 'resumo_perdas' in colheita and isinstance(colheita['resumo_perdas'], list):
                colheita['resumo_perdas'] = tuple(tuple(item) for item in colheita['resumo_perdas'])
        
        registrar_log(f"Colheitas carregadas do JSON: {len(colheitas)} registros", "INFO")
        return colheitas
    except json.JSONDecodeError as e:
        print(f"✗ Erro ao decodificar JSON de colheitas: {e}")
        registrar_log(f"Erro ao decodificar JSON de colheitas: {e}", "ERRO")
        return []
    except Exception as e:
        print(f"✗ Erro ao carregar colheitas: {e}")
        registrar_log(f"Erro ao carregar colheitas: {e}", "ERRO")
        return []


def exportar_relatorio_texto(nome_arquivo, conteudo):
    """
    Exporta um relatório em formato texto
    Escrita de arquivo texto formatado
    
    Parâmetros:
        nome_arquivo (str): nome do arquivo de saída
        conteudo (str): conteúdo do relatório
    
    Retorna:
        bool: True se exportado com sucesso
    """
    try:
        # Adiciona timestamp ao nome do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_completo = f"dados/relatorio_{nome_arquivo}_{timestamp}.txt"
        
        # Cria diretório se não existir
        os.makedirs(os.path.dirname(nome_completo), exist_ok=True)
        
        # Cabeçalho do relatório
        cabecalho = f"""
{'='*70}
RELATÓRIO DE GESTÃO DE COLHEITAS DE CANA-DE-AÇÚCAR
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
{'='*70}

"""
        
        # Escreve no arquivo
        with open(nome_completo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(cabecalho)
            arquivo.write(conteudo)
            arquivo.write(f"\n\n{'='*70}\n")
            arquivo.write("Fim do relatório\n")
            arquivo.write(f"{'='*70}\n")
        
        print(f"\n✓ Relatório exportado: {nome_completo}")
        registrar_log(f"Relatório exportado: {nome_completo}", "INFO")
        return True
    except Exception as e:
        print(f"✗ Erro ao exportar relatório: {e}")
        registrar_log(f"Erro ao exportar relatório: {e}", "ERRO")
        return False


def backup_dados():
    """
    Cria backup dos arquivos de dados
    Cópia de arquivos JSON
    
    Retorna:
        bool: True se backup criado com sucesso
    """
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Backup de fazendas
        if os.path.exists(ARQUIVO_FAZENDAS):
            backup_fazendas = f"dados/backup_fazendas_{timestamp}.json"
            with open(ARQUIVO_FAZENDAS, 'r', encoding='utf-8') as origem:
                conteudo = origem.read()
            with open(backup_fazendas, 'w', encoding='utf-8') as destino:
                destino.write(conteudo)
        
        # Backup de colheitas
        if os.path.exists(ARQUIVO_COLHEITAS):
            backup_colheitas = f"dados/backup_colheitas_{timestamp}.json"
            with open(ARQUIVO_COLHEITAS, 'r', encoding='utf-8') as origem:
                conteudo = origem.read()
            with open(backup_colheitas, 'w', encoding='utf-8') as destino:
                destino.write(conteudo)
        
        print(f"\n✓ Backup criado com sucesso!")
        registrar_log(f"Backup de dados criado: {timestamp}", "INFO")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar backup: {e}")
        registrar_log(f"Erro ao criar backup: {e}", "ERRO")
        return False


def limpar_logs():
    """
    Limpa o arquivo de logs (cria novo arquivo vazio)
    Manipulação de arquivo texto
    """
    try:
        with open(ARQUIVO_LOGS, 'w', encoding='utf-8') as arquivo:
            arquivo.write("")
        
        print("✓ Logs limpos com sucesso")
        registrar_log("Logs limpos", "INFO")
        return True
    except Exception as e:
        print(f"✗ Erro ao limpar logs: {e}")
        return False


def verificar_integridade_arquivos():
    """
    Verifica se os arquivos de dados estão íntegros
    Leitura e validação de arquivos
    
    Retorna:
        dict: status de cada arquivo
    """
    status = {
        'fazendas': 'OK',
        'colheitas': 'OK',
        'logs': 'OK'
    }
    
    # Verifica fazendas
    try:
        if os.path.exists(ARQUIVO_FAZENDAS):
            with open(ARQUIVO_FAZENDAS, 'r', encoding='utf-8') as arquivo:
                json.load(arquivo)
        else:
            status['fazendas'] = 'AUSENTE'
    except json.JSONDecodeError:
        status['fazendas'] = 'CORROMPIDO'
    except Exception:
        status['fazendas'] = 'ERRO'
    
    # Verifica colheitas
    try:
        if os.path.exists(ARQUIVO_COLHEITAS):
            with open(ARQUIVO_COLHEITAS, 'r', encoding='utf-8') as arquivo:
                json.load(arquivo)
        else:
            status['colheitas'] = 'AUSENTE'
    except json.JSONDecodeError:
        status['colheitas'] = 'CORROMPIDO'
    except Exception:
        status['colheitas'] = 'ERRO'
    
    # Verifica logs
    try:
        if os.path.exists(ARQUIVO_LOGS):
            with open(ARQUIVO_LOGS, 'r', encoding='utf-8') as arquivo:
                arquivo.read()
        else:
            status['logs'] = 'AUSENTE'
    except Exception:
        status['logs'] = 'ERRO'
    
    return status


def exibir_status_arquivos():
    """
    Exibe o status dos arquivos de dados
    Procedimento que mostra informações dos arquivos
    """
    print("\n" + "="*70)
    print("📁 STATUS DOS ARQUIVOS DE DADOS")
    print("="*70)
    
    status = verificar_integridade_arquivos()
    
    arquivos = {
        'fazendas': ARQUIVO_FAZENDAS,
        'colheitas': ARQUIVO_COLHEITAS,
        'logs': ARQUIVO_LOGS
    }
    
    for tipo, arquivo in arquivos.items():
        st = status[tipo]
        icone = "✓" if st == "OK" else "✗"
        
        print(f"\n{icone} {tipo.upper()}: {st}")
        print(f"   Arquivo: {arquivo}")
        
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"   Tamanho: {tamanho} bytes")
            
            # Conta registros se for JSON
            if st == "OK" and arquivo.endswith('.json'):
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                        print(f"   Registros: {len(dados)}")
                except:
                    pass
    
    print("\n" + "="*70)


