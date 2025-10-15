"""
Arquivo de configuração do sistema
Contém constantes e configurações gerais
"""

# Configurações de Banco de Dados Oracle
DB_CONFIG = {
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'dsn': 'localhost:1521/XEPDB1',  # Ajuste conforme seu ambiente
    'encoding': 'UTF-8'
}

# Configurações de Arquivos
ARQUIVO_FAZENDAS = 'dados/fazendas.json'
ARQUIVO_COLHEITAS = 'dados/colheitas.json'
ARQUIVO_LOGS = 'dados/logs.txt'

# Tuplas de configuração (dados imutáveis)
TIPOS_COLHEITA = ('manual', 'mecânica', 'mista')
TIPOS_PERDA = ('mecânica', 'raizame', 'palha', 'climática', 'pragas')
VARIEDADES_CANA = ('RB867515', 'RB966928', 'SP813250', 'CTC4', 'CTC20')

# Parâmetros de análise (tupla)
PARAMETROS_ANALISE = (
    ('perda_baixa', 5.0),      # até 5%
    ('perda_media', 10.0),     # 5% a 10%
    ('perda_alta', 15.0),      # 10% a 15%
    ('perda_critica', float('inf'))  # acima de 15%
)

# Produtividade esperada por variedade (dicionário)
PRODUTIVIDADE_ESPERADA = {
    'RB867515': 85.0,
    'RB966928': 90.0,
    'SP813250': 80.0,
    'CTC4': 95.0,
    'CTC20': 92.0
}

# Mensagens do sistema (dicionário)
MENSAGENS = {
    'sucesso_cadastro': '✓ Cadastro realizado com sucesso!',
    'erro_validacao': '✗ Erro de validação: {}',
    'erro_arquivo': '✗ Erro ao manipular arquivo: {}',
    'erro_banco': '✗ Erro no banco de dados: {}',
    'aviso': '⚠️ Atenção: {}',
    'info': 'ℹ️ {}',
}

# Constantes de cálculo
DENSIDADE_CANA = 1.05  # ton/m³
UMIDADE_PADRAO = 0.70  # 70%
ATR_MEDIO = 140.0  # kg ATR/tonelada

# Limites de validação
LIMITES = {
    'area_min': 0.1,
    'area_max': 1000.0,
    'producao_min': 10.0,
    'producao_max': 200.0,
    'perda_min': 0.0,
    'perda_max': 50.0
}

