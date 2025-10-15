"""
Módulo de conexão com banco de dados Oracle
Capítulo 6: Banco de Dados Oracle

NOTA: cx_Oracle é uma dependência OPCIONAL
- O sistema funciona completamente sem ele (usando JSON para persistência)
- Para usar funcionalidades de BD Oracle, instale: pip install cx-Oracle
- Também requer Oracle Instant Client instalado no sistema
"""

try:
    import cx_Oracle  # type: ignore  # Importação opcional
    ORACLE_DISPONIVEL = True
except ImportError:
    ORACLE_DISPONIVEL = False
    print("⚠️ Módulo cx_Oracle não instalado. Funcionalidades de BD limitadas.")

from config import DB_CONFIG
from modulos.arquivo import registrar_log


def testar_conexao():
    """
    Testa a conexão com o banco de dados Oracle
    
    Retorna:
        bool: True se conexão bem-sucedida
    """
    if not ORACLE_DISPONIVEL:
        print("✗ cx_Oracle não está instalado")
        return False
    
    try:
        # Tenta conectar
        conexao = cx_Oracle.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            dsn=DB_CONFIG['dsn'],
            encoding=DB_CONFIG['encoding']
        )
        
        # Testa com uma query simples
        cursor = conexao.cursor()
        cursor.execute("SELECT 1 FROM DUAL")
        cursor.close()
        conexao.close()
        
        print("✓ Conexão com Oracle bem-sucedida!")
        registrar_log("Conexão com Oracle testada com sucesso", "INFO")
        return True
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        registrar_log(f"Erro na conexão com Oracle: {e}", "ERRO")
        return False


def obter_conexao():
    """
    Obtém uma conexão com o banco de dados
    
    Retorna:
        connection: objeto de conexão ou None
    """
    if not ORACLE_DISPONIVEL:
        return None
    
    try:
        conexao = cx_Oracle.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            dsn=DB_CONFIG['dsn'],
            encoding=DB_CONFIG['encoding']
        )
        return conexao
    except Exception as e:
        print(f"✗ Erro ao obter conexão: {e}")
        registrar_log(f"Erro ao obter conexão: {e}", "ERRO")
        return None


def criar_tabelas():
    """
    Cria as tabelas no banco de dados
    DDL - Data Definition Language
    
    Retorna:
        bool: True se criado com sucesso
    """
    if not ORACLE_DISPONIVEL:
        print("✗ cx_Oracle não disponível")
        return False
    
    conexao = obter_conexao()
    if not conexao:
        return False
    
    try:
        cursor = conexao.cursor()
        
        # Tabela de Fazendas
        cursor.execute("""
            CREATE TABLE fazendas (
                id NUMBER PRIMARY KEY,
                nome VARCHAR2(100) NOT NULL,
                proprietario VARCHAR2(100) NOT NULL,
                documento VARCHAR2(20) NOT NULL,
                tipo_documento VARCHAR2(10),
                localizacao VARCHAR2(100),
                area_total NUMBER(10, 2),
                data_cadastro DATE DEFAULT SYSDATE
            )
        """)
        
        # Tabela de Talhões
        cursor.execute("""
            CREATE TABLE talhoes (
                id NUMBER PRIMARY KEY,
                id_fazenda NUMBER NOT NULL,
                codigo VARCHAR2(20) NOT NULL,
                area NUMBER(10, 2) NOT NULL,
                variedade VARCHAR2(20) NOT NULL,
                ano_plantio NUMBER(4),
                status VARCHAR2(20) DEFAULT 'ativo',
                CONSTRAINT fk_fazenda FOREIGN KEY (id_fazenda) 
                    REFERENCES fazendas(id)
            )
        """)
        
        # Tabela de Colheitas
        cursor.execute("""
            CREATE TABLE colheitas (
                id NUMBER PRIMARY KEY,
                id_fazenda NUMBER NOT NULL,
                codigo_talhao VARCHAR2(20) NOT NULL,
                data_colheita DATE NOT NULL,
                tipo_colheita VARCHAR2(20) NOT NULL,
                area_colhida NUMBER(10, 2) NOT NULL,
                variedade VARCHAR2(20),
                quantidade_colhida NUMBER(10, 2) NOT NULL,
                quantidade_perdida NUMBER(10, 2),
                produtividade NUMBER(10, 2),
                percentual_perda_total NUMBER(5, 2),
                status VARCHAR2(50),
                data_registro DATE DEFAULT SYSDATE,
                CONSTRAINT fk_colheita_fazenda FOREIGN KEY (id_fazenda) 
                    REFERENCES fazendas(id)
            )
        """)
        
        # Tabela de Perdas Detalhadas
        cursor.execute("""
            CREATE TABLE perdas_detalhadas (
                id NUMBER PRIMARY KEY,
                id_colheita NUMBER NOT NULL,
                tipo_perda VARCHAR2(50) NOT NULL,
                percentual NUMBER(5, 2) NOT NULL,
                CONSTRAINT fk_perda_colheita FOREIGN KEY (id_colheita) 
                    REFERENCES colheitas(id)
            )
        """)
        
        # Cria sequences para IDs
        cursor.execute("CREATE SEQUENCE seq_fazendas START WITH 1 INCREMENT BY 1")
        cursor.execute("CREATE SEQUENCE seq_talhoes START WITH 1 INCREMENT BY 1")
        cursor.execute("CREATE SEQUENCE seq_colheitas START WITH 1 INCREMENT BY 1")
        cursor.execute("CREATE SEQUENCE seq_perdas START WITH 1 INCREMENT BY 1")
        
        conexao.commit()
        cursor.close()
        conexao.close()
        
        print("✓ Tabelas criadas com sucesso!")
        registrar_log("Tabelas do banco criadas", "INFO")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar tabelas: {e}")
        registrar_log(f"Erro ao criar tabelas: {e}", "ERRO")
        if conexao:
            conexao.close()
        return False


def inserir_fazenda(fazenda):
    """
    Insere uma fazenda no banco de dados
    DML - INSERT
    
    Parâmetro:
        fazenda (dict): dicionário com dados da fazenda
    
    Retorna:
        int: ID da fazenda inserida ou None
    """
    if not ORACLE_DISPONIVEL:
        return None
    
    conexao = obter_conexao()
    if not conexao:
        return None
    
    try:
        cursor = conexao.cursor()
        
        # Query parametrizada (proteção contra SQL injection)
        sql = """
            INSERT INTO fazendas 
                (id, nome, proprietario, documento, tipo_documento, localizacao, area_total)
            VALUES 
                (seq_fazendas.NEXTVAL, :nome, :proprietario, :documento, 
                 :tipo_documento, :localizacao, :area_total)
            RETURNING id INTO :id_out
        """
        
        id_var = cursor.var(cx_Oracle.NUMBER)
        
        cursor.execute(sql, {
            'nome': fazenda['nome'],
            'proprietario': fazenda['proprietario'],
            'documento': fazenda['documento'],
            'tipo_documento': fazenda['tipo_documento'],
            'localizacao': fazenda['localizacao'],
            'area_total': fazenda['area_total'],
            'id_out': id_var
        })
        
        id_inserido = int(id_var.getvalue()[0])
        
        conexao.commit()
        cursor.close()
        conexao.close()
        
        registrar_log(f"Fazenda '{fazenda['nome']}' inserida no BD (ID: {id_inserido})", "INFO")
        return id_inserido
    except Exception as e:
        print(f"✗ Erro ao inserir fazenda: {e}")
        registrar_log(f"Erro ao inserir fazenda: {e}", "ERRO")
        if conexao:
            conexao.rollback()
            conexao.close()
        return None


def inserir_colheita(colheita):
    """
    Insere uma colheita no banco de dados
    DML - INSERT com transação
    
    Parâmetro:
        colheita (dict): dicionário com dados da colheita
    
    Retorna:
        int: ID da colheita inserida ou None
    """
    if not ORACLE_DISPONIVEL:
        return None
    
    conexao = obter_conexao()
    if not conexao:
        return None
    
    try:
        cursor = conexao.cursor()
        
        # Insere colheita principal
        sql_colheita = """
            INSERT INTO colheitas 
                (id, id_fazenda, codigo_talhao, data_colheita, tipo_colheita,
                 area_colhida, variedade, quantidade_colhida, quantidade_perdida,
                 produtividade, percentual_perda_total, status)
            VALUES 
                (seq_colheitas.NEXTVAL, :id_fazenda, :codigo_talhao, 
                 TO_DATE(:data_colheita, 'DD/MM/YYYY'), :tipo_colheita,
                 :area_colhida, :variedade, :quantidade_colhida, :quantidade_perdida,
                 :produtividade, :percentual_perda_total, :status)
            RETURNING id INTO :id_out
        """
        
        id_var = cursor.var(cx_Oracle.NUMBER)
        
        cursor.execute(sql_colheita, {
            'id_fazenda': colheita['id_fazenda'],
            'codigo_talhao': colheita['codigo_talhao'],
            'data_colheita': colheita['data_colheita'],
            'tipo_colheita': colheita['tipo_colheita'],
            'area_colhida': colheita['area_colhida'],
            'variedade': colheita['variedade'],
            'quantidade_colhida': colheita['quantidade_colhida'],
            'quantidade_perdida': colheita['quantidade_perdida'],
            'produtividade': colheita['produtividade'],
            'percentual_perda_total': colheita['percentual_perda_total'],
            'status': colheita['status'],
            'id_out': id_var
        })
        
        id_colheita = int(id_var.getvalue()[0])
        
        # Insere perdas detalhadas
        sql_perdas = """
            INSERT INTO perdas_detalhadas (id, id_colheita, tipo_perda, percentual)
            VALUES (seq_perdas.NEXTVAL, :id_colheita, :tipo_perda, :percentual)
        """
        
        for tipo_perda, percentual in colheita['perdas_detalhadas'].items():
            cursor.execute(sql_perdas, {
                'id_colheita': id_colheita,
                'tipo_perda': tipo_perda,
                'percentual': percentual
            })
        
        conexao.commit()
        cursor.close()
        conexao.close()
        
        registrar_log(f"Colheita ID {id_colheita} inserida no BD", "INFO")
        return id_colheita
    except Exception as e:
        print(f"✗ Erro ao inserir colheita: {e}")
        registrar_log(f"Erro ao inserir colheita: {e}", "ERRO")
        if conexao:
            conexao.rollback()
            conexao.close()
        return None


def buscar_fazendas():
    """
    Busca todas as fazendas do banco de dados
    DML - SELECT
    
    Retorna:
        list: lista de fazendas
    """
    if not ORACLE_DISPONIVEL:
        return []
    
    conexao = obter_conexao()
    if not conexao:
        return []
    
    try:
        cursor = conexao.cursor()
        
        cursor.execute("""
            SELECT id, nome, proprietario, documento, tipo_documento, 
                   localizacao, area_total, data_cadastro
            FROM fazendas
            ORDER BY id
        """)
        
        fazendas = []
        for row in cursor:
            fazenda = {
                'id': row[0],
                'nome': row[1],
                'proprietario': row[2],
                'documento': row[3],
                'tipo_documento': row[4],
                'localizacao': row[5],
                'area_total': float(row[6]) if row[6] else 0,
                'data_cadastro': row[7].strftime('%d/%m/%Y') if row[7] else '',
                'talhoes': []
            }
            fazendas.append(fazenda)
        
        cursor.close()
        conexao.close()
        
        return fazendas
    except Exception as e:
        print(f"✗ Erro ao buscar fazendas: {e}")
        if conexao:
            conexao.close()
        return []


def buscar_colheitas():
    """
    Busca todas as colheitas do banco de dados
    DML - SELECT com JOIN
    
    Retorna:
        list: lista de colheitas
    """
    if not ORACLE_DISPONIVEL:
        return []
    
    conexao = obter_conexao()
    if not conexao:
        return []
    
    try:
        cursor = conexao.cursor()
        
        cursor.execute("""
            SELECT c.id, c.id_fazenda, f.nome, c.codigo_talhao,
                   TO_CHAR(c.data_colheita, 'DD/MM/YYYY'), c.tipo_colheita,
                   c.area_colhida, c.variedade, c.quantidade_colhida,
                   c.quantidade_perdida, c.produtividade,
                   c.percentual_perda_total, c.status,
                   TO_CHAR(c.data_registro, 'DD/MM/YYYY HH24:MI:SS')
            FROM colheitas c
            JOIN fazendas f ON c.id_fazenda = f.id
            ORDER BY c.id
        """)
        
        colheitas = []
        for row in cursor:
            colheita = {
                'id': row[0],
                'id_fazenda': row[1],
                'nome_fazenda': row[2],
                'codigo_talhao': row[3],
                'data_colheita': row[4],
                'tipo_colheita': row[5],
                'area_colhida': float(row[6]),
                'variedade': row[7],
                'quantidade_colhida': float(row[8]),
                'quantidade_perdida': float(row[9]),
                'produtividade': float(row[10]),
                'percentual_perda_total': float(row[11]),
                'status': row[12],
                'data_registro': row[13],
                'perdas_detalhadas': {},
                'resumo_perdas': ()
            }
            
            # Busca perdas detalhadas
            cursor2 = conexao.cursor()
            cursor2.execute("""
                SELECT tipo_perda, percentual
                FROM perdas_detalhadas
                WHERE id_colheita = :id_colheita
            """, {'id_colheita': colheita['id']})
            
            for perda_row in cursor2:
                tipo = perda_row[0]
                perc = float(perda_row[1])
                colheita['perdas_detalhadas'][tipo] = perc
            
            cursor2.close()
            
            # Cria tupla de resumo
            colheita['resumo_perdas'] = tuple(
                sorted(colheita['perdas_detalhadas'].items(), 
                       key=lambda x: x[1], reverse=True)
            )
            
            colheitas.append(colheita)
        
        cursor.close()
        conexao.close()
        
        return colheitas
    except Exception as e:
        print(f"✗ Erro ao buscar colheitas: {e}")
        if conexao:
            conexao.close()
        return []


def atualizar_fazenda(id_fazenda, dados):
    """
    Atualiza dados de uma fazenda
    DML - UPDATE
    
    Parâmetros:
        id_fazenda (int): ID da fazenda
        dados (dict): dados a atualizar
    
    Retorna:
        bool: True se atualizado com sucesso
    """
    if not ORACLE_DISPONIVEL:
        return False
    
    conexao = obter_conexao()
    if not conexao:
        return False
    
    try:
        cursor = conexao.cursor()
        
        # Monta query dinamicamente baseado nos dados fornecidos
        campos = []
        valores = {'id': id_fazenda}
        
        for campo, valor in dados.items():
            campos.append(f"{campo} = :{campo}")
            valores[campo] = valor
        
        sql = f"UPDATE fazendas SET {', '.join(campos)} WHERE id = :id"
        
        cursor.execute(sql, valores)
        
        linhas_afetadas = cursor.rowcount
        
        conexao.commit()
        cursor.close()
        conexao.close()
        
        if linhas_afetadas > 0:
            registrar_log(f"Fazenda ID {id_fazenda} atualizada no BD", "INFO")
            return True
        return False
    except Exception as e:
        print(f"✗ Erro ao atualizar fazenda: {e}")
        if conexao:
            conexao.rollback()
            conexao.close()
        return False


def deletar_colheita(id_colheita):
    """
    Deleta uma colheita do banco de dados
    DML - DELETE com transação
    
    Parâmetro:
        id_colheita (int): ID da colheita
    
    Retorna:
        bool: True se deletado com sucesso
    """
    if not ORACLE_DISPONIVEL:
        return False
    
    conexao = obter_conexao()
    if not conexao:
        return False
    
    try:
        cursor = conexao.cursor()
        
        # Deleta perdas detalhadas primeiro (integridade referencial)
        cursor.execute("""
            DELETE FROM perdas_detalhadas WHERE id_colheita = :id_colheita
        """, {'id_colheita': id_colheita})
        
        # Deleta colheita
        cursor.execute("""
            DELETE FROM colheitas WHERE id = :id_colheita
        """, {'id_colheita': id_colheita})
        
        linhas_afetadas = cursor.rowcount
        
        conexao.commit()
        cursor.close()
        conexao.close()
        
        if linhas_afetadas > 0:
            registrar_log(f"Colheita ID {id_colheita} deletada do BD", "INFO")
            return True
        return False
    except Exception as e:
        print(f"✗ Erro ao deletar colheita: {e}")
        if conexao:
            conexao.rollback()
            conexao.close()
        return False


def sincronizar_dados_bd(fazendas_lista, colheitas_lista):
    """
    Sincroniza dados da memória com o banco de dados
    Operação completa: DELETE + INSERT (refresh)
    
    Parâmetros:
        fazendas_lista (list): lista de fazendas
        colheitas_lista (list): lista de colheitas
    
    Retorna:
        bool: True se sincronizado com sucesso
    """
    if not ORACLE_DISPONIVEL:
        print("✗ cx_Oracle não disponível")
        return False
    
    conexao = obter_conexao()
    if not conexao:
        return False
    
    try:
        print("\n🔄 Sincronizando dados com o banco...")
        
        # Limpa dados existentes (em ordem devido às FKs)
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM perdas_detalhadas")
        cursor.execute("DELETE FROM colheitas")
        cursor.execute("DELETE FROM talhoes")
        cursor.execute("DELETE FROM fazendas")
        
        # Reseta sequences
        cursor.execute("DROP SEQUENCE seq_fazendas")
        cursor.execute("DROP SEQUENCE seq_talhoes")
        cursor.execute("DROP SEQUENCE seq_colheitas")
        cursor.execute("DROP SEQUENCE seq_perdas")
        
        cursor.execute("CREATE SEQUENCE seq_fazendas START WITH 1 INCREMENT BY 1")
        cursor.execute("CREATE SEQUENCE seq_talhoes START WITH 1 INCREMENT BY 1")
        cursor.execute("CREATE SEQUENCE seq_colheitas START WITH 1 INCREMENT BY 1")
        cursor.execute("CREATE SEQUENCE seq_perdas START WITH 1 INCREMENT BY 1")
        
        # Insere fazendas
        for fazenda in fazendas_lista:
            inserir_fazenda(fazenda)
        
        # Insere colheitas
        for colheita in colheitas_lista:
            inserir_colheita(colheita)
        
        conexao.commit()
        cursor.close()
        conexao.close()
        
        print(f"✓ Sincronização concluída!")
        print(f"  Fazendas: {len(fazendas_lista)}")
        print(f"  Colheitas: {len(colheitas_lista)}")
        
        registrar_log("Dados sincronizados com o banco", "INFO")
        return True
    except Exception as e:
        print(f"✗ Erro na sincronização: {e}")
        if conexao:
            conexao.rollback()
            conexao.close()
        return False

