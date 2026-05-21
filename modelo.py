import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect('erp_estoque.db')

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabela de Produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    ''')
    
    # Tabela de Vendas (Necessária para alimentar o Dashboard com dados reais)
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
    conn.commit()
    conn.close()

def inserir_produto(nome, preco, qtd):
    # Uso de marcadores seguros (?, ?) para prevenir Injeção SQL
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, qtd))
    conn.commit()
    conn.close()

def buscar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, quantidade, preco FROM produtos")
    resultados = cursor.fetchall() # Retorna a lista
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