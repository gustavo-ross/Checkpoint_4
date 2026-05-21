import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect('erp_estoque.db')

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            quantidade INTEGER,
            valor_total REAL,
            data_venda DATE,
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            preco_antigo REAL,
            preco_novo REAL,
            data_alteracao DATETIME,
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def verificar_produto_existente(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM produtos WHERE LOWER(nome) = LOWER(?)", (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def inserir_produto(nome, preco, qtd):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, qtd))
    conn.commit()
    conn.close()

def buscar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, quantidade, preco FROM produtos")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def buscar_produtos_por_nome(termo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, quantidade, preco FROM produtos WHERE nome LIKE ?", (termo,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def deletar_produto(id_produto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
    conn.commit()
    conn.close()

def registrar_venda_db(produto_id, quantidade, valor_total):
    conn = conectar()
    cursor = conn.cursor()
    data_atual = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute("INSERT INTO vendas (produto_id, quantidade, valor_total, data_venda) VALUES (?, ?, ?, ?)",
                   (produto_id, quantidade, valor_total, data_atual))
    
    cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))
    conn.commit()
    conn.close()

def buscar_vendas_dashboard():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(valor_total), SUM(quantidade) FROM vendas")
    totais = cursor.fetchone()
    
    cursor.execute("SELECT data_venda, SUM(valor_total) FROM vendas GROUP BY data_venda ORDER BY data_venda")
    vendas_dia = cursor.fetchall()
    
    cursor.execute('''
        SELECT p.nome, SUM(v.quantidade) as qtd_vendida 
        FROM vendas v 
        JOIN produtos p ON v.produto_id = p.id 
        GROUP BY v.produto_id 
        ORDER BY qtd_vendida DESC LIMIT 5
    ''')
    top_produtos = cursor.fetchall()
    
    conn.close()
    return totais, vendas_dia, top_produtos

def atualizar_preco_produto(produto_id, novo_preco):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT preco FROM produtos WHERE id = ?", (produto_id,))
    resultado = cursor.fetchone()
    
    if not resultado:
        conn.close()
        return False
        
    preco_antigo = resultado[0]
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    cursor.execute('''
        INSERT INTO historico_precos (produto_id, preco_antigo, preco_novo, data_alteracao) 
        VALUES (?, ?, ?, ?)
    ''', (produto_id, preco_antigo, novo_preco, data_atual))
    
    cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (novo_preco, produto_id))
    
    conn.commit()
    conn.close()
    return True

def buscar_historico():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT h.id, p.nome, h.preco_antigo, h.preco_novo, h.data_alteracao 
        FROM historico_precos h
        JOIN produtos p ON h.produto_id = p.id
        ORDER BY h.id DESC
    ''')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def buscar_historico_por_produto(termo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT h.id, p.nome, h.preco_antigo, h.preco_novo, h.data_alteracao 
        FROM historico_precos h
        JOIN produtos p ON h.produto_id = p.id
        WHERE p.nome LIKE ?
        ORDER BY h.id DESC
    ''', (termo,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados