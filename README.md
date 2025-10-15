# FIAP - Faculdade de Informática e Administração Paulista

<img src="assets/logo-fiap.png" alt="FIAP Logo" width="200"/>

# Sistema de Gestão de Perdas na Colheita de Cana-de-Açúcar

## Curso Superior de Tecnologia em Inteligência Artificial

## 👨‍🎓 Integrante:

* Ricardo Rodriguez Frugoni de Souza

## 👨‍🏫 Coordenador:

* Andre Godoi Chiovato

## 📜 Descrição

Este projeto foca na **redução e gestão de perdas na colheita de cana-de-açúcar**, um dos principais desafios do setor sucroalcooleiro brasileiro.

### Contexto do Problema

O Brasil é líder mundial na produção de cana-de-açúcar. No entanto, as perdas na colheita mecânica podem chegar a **15% da produção**, enquanto na colheita manual raramente ultrapassam 5%. Em São Paulo, isso representa uma perda anual de aproximadamente **R$ 20 milhões**.

### Solução Proposta

Sistema completo de gestão e análise de perdas na colheita de cana, que permite:

* **Cadastro de Fazendas e Talhões**: Registro completo de propriedades rurais com divisão em talhões
* **Registro de Colheitas**: Documentação detalhada de cada colheita com método utilizado e quantidade
* **Análise de Perdas**: Registro detalhado de perdas por tipo (mecânica, raizame, palha, climática, pragas)
* **Comparação de Métodos**: Análise comparativa entre colheita manual vs mecânica
* **Sistema de Recomendações**: Sugestões automáticas baseadas em análise de dados para redução de perdas
* **Relatórios e Dashboard**: Visualização clara de KPIs e indicadores importantes
* **Persistência de Dados**: Armazenamento em JSON e integração com Oracle Database

### Funcionalidades Principais

1. **Validação Rigorosa**: CPF/CNPJ, datas, valores numéricos e tipos de entrada
2. **Análise Preditiva**: Identificação de padrões e sugestões de melhorias
3. **Comparação Automática**: Análise de desempenho por método, variedade e talhão
4. **Gestão de Arquivos**: Backup automático, logs de operações e exportação de relatórios
5. **Integração com Oracle**: Operações CRUD completas com transações

### Tecnologias Aplicadas

O projeto demonstra a aplicação de conceitos fundamentais de Python:

* **Subalgoritmos**: Funções com passagem de parâmetros, procedimentos, validações
* **Estruturas de Dados**: Listas, tuplas, dicionários e matrizes
* **Manipulação de Arquivos**: Leitura/escrita de JSON e arquivos texto com tratamento de exceções
* **Banco de Dados Oracle**: Conexão cx_Oracle, operações DDL/DML, transações

## 📁 Estrutura de pastas

```
Cap6_Python_e_alem/
│
├── .github/                    # Configurações do GitHub
├── assets/                     # Imagens e elementos visuais
├── config/                     # Arquivos de configuração
│   └── config.py              # Configurações gerais do sistema
│
├── document/                   # Documentação do projeto
│   └── other/                 # Documentos complementares
│
├── scripts/                    # Scripts auxiliares
│   └── sql/                   # Scripts SQL
│       └── create_tables.sql  # Criação das tabelas Oracle
│
├── src/                        # Código fonte
│   ├── modulos/               # Módulos do sistema
│   │   ├── __init__.py
│   │   ├── validacao.py       # Validações de dados
│   │   ├── fazenda.py         # Gestão de fazendas e talhões
│   │   ├── colheita.py        # Gestão de colheitas
│   │   ├── analise.py         # Análises e relatórios
│   │   ├── arquivo.py         # Manipulação de arquivos
│   │   └── database.py        # Conexão com Oracle
│   │
│   ├── dados/                 # Dados do sistema (não versionado)
│   │   └── .gitkeep
│   │
│   └── main.py                # Arquivo principal
│
├── .gitattributes             # Configuração Git
├── .gitignore                 # Arquivos ignorados
├── README.md                  # Este arquivo
└── requirements.txt           # Dependências Python
```

### Descrição das Pastas

* **.github**: Arquivos de configuração do GitHub para automação e CI/CD
* **assets**: Imagens, logos e outros elementos não-estruturados do repositório
* **config**: Arquivos de configuração (constantes, parâmetros, credenciais)
* **document**: Documentação completa do projeto, diagramas e manuais
* **scripts**: Scripts auxiliares (SQL, deploy, migrações, backups)
* **src**: Todo o código fonte Python do projeto

## 🔧 Como executar o código

### Pré-requisitos

* Python 3.8 ou superior
* Oracle Instant Client (para conexão com banco de dados)
* cx_Oracle 8.3.0 ou superior

### Instalação

1. **Clone o repositório**

```bash
git clone <url-do-repositorio>
cd Cap6_Python_e_alem
```

2. **Instale as dependências**

```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados Oracle**

   * Edite `config/config.py` com suas credenciais Oracle
   * Execute o script SQL de criação das tabelas:

```bash
# No SQL Developer ou SQL*Plus
@scripts/sql/create_tables.sql
```

4. **Execute o sistema**

```bash
cd src
python main.py
```

### Estrutura de Navegação

O sistema apresenta um menu interativo com as seguintes opções:

```
MENU PRINCIPAL

1 - Gestão de Fazendas
2 - Gestão de Talhões  
3 - Registro de Colheitas
4 - Análises e Relatórios
5 - Recomendações
6 - Gerenciamento de Arquivos
7 - Banco de Dados Oracle
8 - Dados de Exemplo
0 - Sair
```

### Dados de Exemplo

Para facilitar os testes, o sistema inclui a opção de carregar dados de exemplo (opção 8 do menu principal):

* 3 fazendas cadastradas
* 5 talhões com diferentes variedades de cana
* 5 registros de colheitas com perdas variadas

## 📋 Validações Implementadas

O sistema possui validações rigorosas para garantir a integridade dos dados:

* **CPF**: Validação de formato e dígitos verificadores
* **CNPJ**: Validação de formato e dígitos verificadores
* **Datas**: Formato DD/MM/AAAA e coerência temporal
* **Valores Numéricos**: Ranges válidos e números positivos
* **Tipos de Entrada**: Validação de tipos (int, float, string)
* **Enumerações**: Tipos de colheita, variedades de cana, tipos de perda

## 🗃 Histórico de lançamentos

* 0.2.0 - 15/10/2024
    * Reorganização seguindo template FIAP oficial
    * Remoção de emojis do código
    * Criação de estrutura de pastas padronizada
* 0.1.0 - 10/10/2024
    * Versão inicial do projeto
    * Implementação completa dos requisitos Cap 3-6
    * Integração com Oracle Database

## 📋 Licença

Sistema de Gestão de Colheitas por FIAP está licenciado sobre Attribution 4.0 International.

---

**Nota**: Este sistema demonstra a aplicação prática de Python no agronegócio, contribuindo para a redução de perdas e aumento da eficiência na produção de cana-de-açúcar, um dos pilares da economia brasileira.
