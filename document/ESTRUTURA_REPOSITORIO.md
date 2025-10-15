# Estrutura do Repositório - Template FIAP

Este documento detalha a organização dos arquivos no repositório seguindo o **template oficial da FIAP**.

## 📦 Arquivos para Enviar ao Repositório

### 📄 Raiz do Projeto

```
✅ .gitattributes          # Configurações de normalização Git
✅ .gitignore              # Arquivos ignorados pelo Git
✅ README.md               # Documentação principal
✅ requirements.txt        # Dependências Python
```

### 📁 Pasta `.github/`

```
✅ .github/README.md       # Documentação sobre configurações GitHub
```

### 📁 Pasta `assets/`

```
✅ assets/.gitkeep         # Mantém pasta no repositório
```

_Esta pasta é destinada a imagens, logos e elementos visuais._

### 📁 Pasta `config/`

```
✅ config/config.py        # Configurações gerais do sistema
```

### 📁 Pasta `document/`

```
✅ document/README.md                    # Índice da documentação
✅ document/ESTRUTURA_REPOSITORIO.md     # Este arquivo
✅ document/other/                       # Pasta para docs complementares
```

### 📁 Pasta `scripts/`

```
✅ scripts/sql/create_tables.sql    # Script de criação do banco Oracle
```

### 📁 Pasta `src/`

```
✅ src/main.py                 # Arquivo principal

✅ src/modulos/                # Módulos do sistema
    ├── __init__.py           # Inicializador
    ├── validacao.py          # Validações
    ├── fazenda.py            # Gestão de fazendas
    ├── colheita.py           # Gestão de colheitas
    ├── analise.py            # Análises e relatórios
    ├── arquivo.py            # Manipulação de arquivos
    └── database.py           # Conexão Oracle

✅ src/dados/.gitkeep          # Mantém pasta no repositório
```

---

## ❌ Arquivos NÃO Versionados

Estes arquivos são ignorados pelo `.gitignore`:

```
❌ __pycache__/                # Cache Python
❌ .venv/                      # Ambiente virtual
❌ src/dados/*.json            # Dados gerados
❌ src/dados/*.txt             # Logs
❌ *.log                       # Arquivos de log
❌ config/config_local.py      # Configurações locais
```

---

## 📊 Resumo

### Total de Arquivos Essenciais: **20 arquivos**

| Categoria | Quantidade |
|-----------|------------|
| Raiz | 4 |
| .github | 1 |
| assets | 1 |
| config | 1 |
| document | 3 |
| scripts/sql | 1 |
| src | 8 |
| src/dados | 1 |

---

## 🔧 Como Usar Este Repositório

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd Cap6_Python_e_alem
```

### 2. Crie um ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o Oracle
- Edite `config/config.py` com suas credenciais
- Execute `scripts/sql/create_tables.sql` no Oracle

### 5. Execute o sistema
```bash
cd src
python main.py
```

---

## 📝 Notas Importantes

1. **Não envie a pasta `.venv`** - Cada desenvolvedor deve criar seu próprio ambiente virtual
2. **Não envie arquivos `__pycache__`** - São gerados automaticamente pelo Python
3. **Não envie dados sensíveis** - Use `config_local.py` para configurações locais
4. **Os erros de sintaxe no main.py** são propositais para exercício dos alunos

---

## 🎯 Template FIAP

Este projeto segue o template oficial disponível em:
[https://github.com/agodoi/templateFiapVfinal](https://github.com/agodoi/templateFiapVfinal)

---

**Autor**: Ricardo Rodriguez Frugoni de Souza  
**Curso**: Tecnologia em Inteligência Artificial - FIAP  
**Coordenador**: Andre Godoi Chiovato  
**Fase**: 2 - Cap 6 - Python e Além

