import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect('erp_estoque.db')

def criar_tabelas():
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        # Adicionado o campo 'ativo' com valor padrão 1 (Significa que o produto está ativo)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                ativo INTEGER DEFAULT 1
            )
        ''')
        
        # Comando de segurança: Caso o banco já exista, adiciona a nova coluna 'ativo' sem quebrar o histórico existente
        try:
            cursor.execute("ALTER TABLE produtos ADD COLUMN ativo INTEGER DEFAULT 1")
        except sqlite3.OperationalError:
            pass # A coluna já existe, ignora o erro
        
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
        
        conexao.commit()
    except sqlite3.Error as erro:
        print(f"❌ Erro ao criar tabelas: {erro}")
    finally:
        if conexao:
            conexao.close()

def verificar_produto_existente(nome):
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Filtra apenas por duplicatas que estejam ativas no momento
        cursor.execute("SELECT id FROM produtos WHERE LOWER(nome) = LOWER(?) AND ativo = 1", (nome,))
        resultado = cursor.fetchone()
        return resultado is not None
    except sqlite3.Error as erro:
        print(f"❌ Erro ao verificar duplicata: {erro}")
        return False
    finally:
        if conexao:
            conexao.close()

def inserir_produto(nome, preco, qtd):
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, qtd))
        conexao.commit()
    except sqlite3.Error as erro:
        print(f"❌ Erro ao cadastrar produto: {erro}")
    finally:
        if conexao:
            conexao.close()

def buscar_produtos():
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Traz apenas os produtos que não foram removidos logicamente
        cursor.execute("SELECT id, nome, quantidade, preco FROM produtos WHERE ativo = 1")
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as erro:
        print(f"❌ Erro ao buscar produtos: {erro}")
        return []
    finally:
        if conexao:
            conexao.close()

def buscar_produtos_por_nome(termo):
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Busca por nome respeitando apenas os itens ativos no estoque
        cursor.execute("SELECT id, nome, quantidade, preco FROM produtos WHERE nome LIKE ? AND ativo = 1", (termo,))
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as erro:
        print(f"❌ Erro na pesquisa de produtos: {erro}")
        return []
    finally:
        if conexao:
            conexao.close()

def deletar_produto(id_produto):
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # CORREÇÃO AQUI: Em vez de DELETE, fazemos um UPDATE desativando o item!
        cursor.execute("UPDATE produtos SET ativo = 0 WHERE id = ?", (id_produto,))
        conexao.commit()
    except sqlite3.Error as erro:
        print(f"❌ Erro ao desativar produto: {erro}")
    finally:
        if conexao:
            conexao.close()

def registrar_venda_db(produto_id, quantidade, valor_total):
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        data_atual = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("INSERT INTO vendas (produto_id, quantidade, valor_total, data_venda) VALUES (?, ?, ?, ?)",
                       (produto_id, quantidade, valor_total, data_atual))
        
        cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))
        conexao.commit()
    except sqlite3.Error as erro:
        print(f"❌ Erro ao registrar venda no banco: {erro}")
    finally:
        if conexao:
            conexao.close()

def buscar_vendas_dashboard():
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT SUM(valor_total), SUM(quantidade) FROM vendas")
        totais = cursor.fetchone()
        if totais[0] is None: 
            totais = (0.0, 0)
        
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
        
        return totais, vendas_dia, top_produtos
    except sqlite3.Error as erro:
        print(f"❌ Erro ao carregar dashboard: {erro}")
        return (0.0, 0), [], []
    finally:
        if conexao:
            conexao.close()

def buscar_todas_vendas():
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT 
                v.id, 
                p.nome, 
                v.quantidade, 
                (v.valor_total / v.quantidade) AS preco_unitario, 
                v.valor_total, 
                v.data_venda
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.id DESC
        ''')
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as erro:
        print(f"❌ Erro ao buscar lista de vendas: {erro}")
        return []
    finally:
        if conexao:
            conexao.close()

def atualizar_preco_produto(produto_id, novo_preco):
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT preco FROM produtos WHERE id = ?", (produto_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            return False
            
        preco_antigo = resultado[0]
        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        cursor.execute('''
            INSERT INTO historico_precos (produto_id, preco_antigo, preco_novo, data_alteracao) 
            VALUES (?, ?, ?, ?)
        ''', (produto_id, preco_antigo, novo_preco, data_atual))
        
        cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (novo_preco, produto_id))
        
        conexao.commit()
        return True
    except sqlite3.Error as erro:
        print(f"❌ Erro ao atualizar preço: {erro}")
        return False
    finally:
        if conexao:
            conexao.close()

def buscar_historico():
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT h.id, p.nome, h.preco_antigo, h.preco_novo, h.data_alteracao 
            FROM historico_precos h
            JOIN produtos p ON h.produto_id = p.id
            ORDER BY h.id DESC
        ''')
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as erro:
        print(f"❌ Erro ao carregar histórico: {erro}")
        return []
    finally:
        if conexao:
            conexao.close()

def buscar_historico_por_produto(termo):
    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT h.id, p.nome, h.preco_antigo, h.preco_novo, h.data_alteracao 
            FROM historico_precos h
            JOIN produtos p ON h.produto_id = p.id
            WHERE p.nome LIKE ?
            ORDER BY h.id DESC
        ''', (termo,))
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as erro:
        print(f"❌ Erro na pesquisa do histórico: {erro}")
        return []
    finally:
        if conexao:
            conexao.close()