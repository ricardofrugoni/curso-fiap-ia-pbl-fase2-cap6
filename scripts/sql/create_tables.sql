-- Script de criação das tabelas para o Sistema de Gestão de Colheitas
-- Banco de Dados: Oracle

-- Limpa objetos existentes (se houver)
DROP TABLE perdas_detalhadas CASCADE CONSTRAINTS;
DROP TABLE colheitas CASCADE CONSTRAINTS;
DROP TABLE talhoes CASCADE CONSTRAINTS;
DROP TABLE fazendas CASCADE CONSTRAINTS;

DROP SEQUENCE seq_fazendas;
DROP SEQUENCE seq_talhoes;
DROP SEQUENCE seq_colheitas;
DROP SEQUENCE seq_perdas;

-- Tabela de Fazendas
CREATE TABLE fazendas (
    id NUMBER PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    proprietario VARCHAR2(100) NOT NULL,
    documento VARCHAR2(20) NOT NULL UNIQUE,
    tipo_documento VARCHAR2(10) CHECK (tipo_documento IN ('CPF', 'CNPJ')),
    localizacao VARCHAR2(100),
    area_total NUMBER(10, 2) DEFAULT 0,
    data_cadastro DATE DEFAULT SYSDATE
);

-- Tabela de Talhões
CREATE TABLE talhoes (
    id NUMBER PRIMARY KEY,
    id_fazenda NUMBER NOT NULL,
    codigo VARCHAR2(20) NOT NULL,
    area NUMBER(10, 2) NOT NULL CHECK (area > 0),
    variedade VARCHAR2(20) NOT NULL,
    ano_plantio NUMBER(4) NOT NULL,
    status VARCHAR2(20) DEFAULT 'ativo',
    CONSTRAINT fk_fazenda FOREIGN KEY (id_fazenda) 
        REFERENCES fazendas(id) ON DELETE CASCADE,
    CONSTRAINT uk_talhao UNIQUE (id_fazenda, codigo)
);

-- Tabela de Colheitas
CREATE TABLE colheitas (
    id NUMBER PRIMARY KEY,
    id_fazenda NUMBER NOT NULL,
    codigo_talhao VARCHAR2(20) NOT NULL,
    data_colheita DATE NOT NULL,
    tipo_colheita VARCHAR2(20) NOT NULL 
        CHECK (tipo_colheita IN ('manual', 'mecânica', 'mista')),
    area_colhida NUMBER(10, 2) NOT NULL CHECK (area_colhida > 0),
    variedade VARCHAR2(20),
    quantidade_colhida NUMBER(10, 2) NOT NULL CHECK (quantidade_colhida > 0),
    quantidade_perdida NUMBER(10, 2) DEFAULT 0,
    produtividade NUMBER(10, 2),
    percentual_perda_total NUMBER(5, 2) DEFAULT 0,
    status VARCHAR2(50),
    data_registro DATE DEFAULT SYSDATE,
    CONSTRAINT fk_colheita_fazenda FOREIGN KEY (id_fazenda) 
        REFERENCES fazendas(id) ON DELETE CASCADE
);

-- Tabela de Perdas Detalhadas
CREATE TABLE perdas_detalhadas (
    id NUMBER PRIMARY KEY,
    id_colheita NUMBER NOT NULL,
    tipo_perda VARCHAR2(50) NOT NULL,
    percentual NUMBER(5, 2) NOT NULL CHECK (percentual >= 0),
    CONSTRAINT fk_perda_colheita FOREIGN KEY (id_colheita) 
        REFERENCES colheitas(id) ON DELETE CASCADE
);

-- Sequences para auto-incremento
CREATE SEQUENCE seq_fazendas START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_talhoes START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_colheitas START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_perdas START WITH 1 INCREMENT BY 1 NOCACHE;

-- Índices para melhorar performance
CREATE INDEX idx_colheitas_fazenda ON colheitas(id_fazenda);
CREATE INDEX idx_colheitas_data ON colheitas(data_colheita);
CREATE INDEX idx_talhoes_fazenda ON talhoes(id_fazenda);
CREATE INDEX idx_perdas_colheita ON perdas_detalhadas(id_colheita);

-- Comentários nas tabelas
COMMENT ON TABLE fazendas IS 'Cadastro de fazendas produtoras de cana-de-açúcar';
COMMENT ON TABLE talhoes IS 'Divisão das fazendas em talhões de produção';
COMMENT ON TABLE colheitas IS 'Registro de colheitas realizadas';
COMMENT ON TABLE perdas_detalhadas IS 'Detalhamento de perdas por tipo';

-- View para relatórios
CREATE OR REPLACE VIEW vw_resumo_colheitas AS
SELECT 
    f.nome AS fazenda,
    f.localizacao,
    c.codigo_talhao,
    c.variedade,
    c.data_colheita,
    c.tipo_colheita,
    c.area_colhida,
    c.quantidade_colhida,
    c.produtividade,
    c.percentual_perda_total,
    c.status
FROM colheitas c
JOIN fazendas f ON c.id_fazenda = f.id
ORDER BY c.data_colheita DESC;

-- View para análise de perdas por método
CREATE OR REPLACE VIEW vw_perdas_por_metodo AS
SELECT 
    tipo_colheita,
    COUNT(*) AS total_colheitas,
    ROUND(AVG(produtividade), 2) AS produtividade_media,
    ROUND(AVG(percentual_perda_total), 2) AS perda_media,
    ROUND(SUM(quantidade_colhida), 2) AS producao_total,
    ROUND(SUM(quantidade_perdida), 2) AS perda_total
FROM colheitas
GROUP BY tipo_colheita;

COMMIT;

-- Mensagem de sucesso
SELECT 'Tabelas criadas com sucesso!' AS status FROM DUAL;


