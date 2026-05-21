import modelo

def inicializar_sistema():
    modelo.criar_tabelas()

def processar_cadastro(nome, q_txt, p_txt):
    if nome == "" or q_txt == "" or p_txt == "":
        return False, "Todos os campos devem ser preenchidos!"
        
    if modelo.verificar_produto_existente(nome):
        return False, f"O produto '{nome}' já está cadastrado no estoque!"
    
    try:
        preco = float(p_txt.replace(',', '.'))
        qtd = int(q_txt)
        if preco < 0 or qtd < 0:
            return False, "Valores não podem ser negativos."
        modelo.inserir_produto(nome, preco, qtd)
        return True, "Produto cadastrado com sucesso!"
    except ValueError:
        return False, "Erro nos números! Formato inválido."

def processar_remocao(id_txt):
    if id_txt == "":
        return False, "O ID do produto não pode estar vazio."
    try:
        id_produto = int(id_txt)
        modelo.deletar_produto(id_produto)
        return True, "Produto removido do estoque."
    except ValueError:
        return False, "ID inválido. Digite um número inteiro."

def listar_produtos():
    return modelo.buscar_produtos()

def pesquisar_produtos(termo):
    if not termo.strip():
        return listar_produtos()
    return modelo.buscar_produtos_por_nome(f"%{termo}%")

def processar_venda(produto_nome, q_txt):
    if not produto_nome or produto_nome == "Selecione":
        return False, "Selecione um produto da lista."
    if q_txt == "":
        return False, "Digite a quantidade que deseja vender."
    try:
        qtd_venda = int(q_txt)
        if qtd_venda <= 0:
            return False, "A quantidade deve ser maior que zero."
        
        produtos = modelo.buscar_produtos()
        produto_selecionado = next((p for p in produtos if p[1] == produto_nome), None)
        
        if not produto_selecionado:
            return False, "Produto não encontrado no sistema."
            
        id_prod, nome_prod, estoque, preco = produto_selecionado
        if qtd_venda > estoque:
            return False, f"Estoque insuficiente. Restam {estoque} unidades."
            
        valor_total = qtd_venda * preco
        modelo.registrar_venda_db(id_prod, qtd_venda, valor_total)
        return True, "Venda registrada com sucesso!"
    except ValueError:
        return False, "Quantidade com formato inválido."

def obter_dados_dashboard():
    totais, vendas_dia, top_produtos = modelo.buscar_vendas_dashboard()
    faturamento = totais[0] if totais[0] else 0.0
    qtd_vendida = totais[1] if totais[1] else 0
    datas = [linha[0][-2:] for linha in vendas_dia]
    valores_dia = [linha[1] for linha in vendas_dia]
    nomes_prod = [linha[0] for linha in top_produtos]
    qtd_prod = [linha[1] for linha in top_produtos]
    return faturamento, qtd_vendida, datas, valores_dia, nomes_prod, qtd_prod

def processar_edicao_preco(produto_nome, p_txt):
    if not produto_nome or produto_nome == "Selecione":
        return False, "Selecione um produto da lista."
    if p_txt == "":
        return False, "Digite o novo valor de venda."
    try:
        novo_preco = float(p_txt.replace(',', '.'))
        if novo_preco < 0:
            return False, "O valor não pode ser negativo."
            
        produtos = modelo.buscar_produtos()
        produto_selecionado = next((p for p in produtos if p[1] == produto_nome), None)
        
        if not produto_selecionado:
            return False, "Produto não encontrado no sistema."
            
        id_prod = produto_selecionado[0]
        sucesso = modelo.atualizar_preco_produto(id_prod, novo_preco)
        
        if sucesso:
            return True, "Valor do produto alterado com sucesso!"
        else:
            return False, "Erro ao alterar o valor no banco."
            
    except ValueError:
        return False, "Valor com formato inválido."

def listar_historico():
    return modelo.buscar_historico()

def pesquisar_historico(termo):
    if not termo.strip():
        return listar_historico()
    return modelo.buscar_historico_por_produto(f"%{termo}%")