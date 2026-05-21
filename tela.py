import customtkinter as ctk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import controlador

# Cores baseadas nos seus wireframes
COR_AZUL = "#1a73e8"
COR_VERDE = "#0f9d58"
COR_VERMELHA = "#b31412"
COR_FUNDO = "#f5f5f5"

ctk.set_appearance_mode("Light") # Mantendo a estética clara proposta

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão - ERP")
        self.geometry("1200x800")
        self.configure(fg_color=COR_FUNDO)
        
        controlador.inicializar_sistema()
        
        self.setup_header()
        self.container_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.container_principal.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.mostrar_tela_vendas()

    def setup_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        # Menu de Navegação
        nav_frame = ctk.CTkFrame(header_frame, fg_color="#e0e0e0", corner_radius=8)
        nav_frame.pack(side="left")
        
        self.btn_nav_vendas = ctk.CTkButton(nav_frame, text="Vendas", fg_color=COR_AZUL, text_color="white", width=120, command=self.mostrar_tela_vendas)
        self.btn_nav_vendas.pack(side="left", padx=2, pady=2)
        
        self.btn_nav_produtos = ctk.CTkButton(nav_frame, text="Produtos", fg_color="transparent", text_color="black", width=120, hover_color="#d6d6d6", command=self.mostrar_tela_produtos)
        self.btn_nav_produtos.pack(side="left", padx=2, pady=2)
        
        # Botões de Ação
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")
        
        ctk.CTkButton(actions_frame, text="Registrar venda", fg_color=COR_AZUL, command=self.abrir_modal_venda).pack(side="right", padx=5)
        ctk.CTkButton(actions_frame, text="Registrar entrada", fg_color=COR_VERDE, command=self.abrir_modal_entrada).pack(side="right", padx=5)
        ctk.CTkButton(actions_frame, text="Remover produto", fg_color=COR_VERMELHA, command=self.abrir_modal_remover).pack(side="right", padx=5)

    def limpar_container(self):
        for widget in self.container_principal.winfo_children():
            widget.destroy()

    def atualizar_botoes_nav(self, aba_ativa):
        if aba_ativa == "Vendas":
            self.btn_nav_vendas.configure(fg_color=COR_AZUL, text_color="white")
            self.btn_nav_produtos.configure(fg_color="transparent", text_color="black")
        else:
            self.btn_nav_produtos.configure(fg_color=COR_AZUL, text_color="white")
            self.btn_nav_vendas.configure(fg_color="transparent", text_color="black")

    # ==================== TELAS PRINCIPAIS ====================
    def mostrar_tela_vendas(self):
        self.limpar_container()
        self.atualizar_botoes_nav("Vendas")
        
        faturamento, qtd_vendida, datas, valores_dia, nomes_prod, qtd_prod = controlador.obter_dados_dashboard()
        
        # Cards de Resumo
        cards_frame = ctk.CTkFrame(self.container_principal, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        
        card1 = ctk.CTkFrame(cards_frame, fg_color="white", corner_radius=8, border_width=1, border_color="#d9d9d9")
        card1.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(card1, text="Vendas deste mês", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(15,0))
        ctk.CTkLabel(card1, text=f"R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), font=("Arial", 36, "bold")).pack(anchor="w", padx=20, pady=(0,15))
        
        card2 = ctk.CTkFrame(cards_frame, fg_color="white", corner_radius=8, border_width=1, border_color="#d9d9d9")
        card2.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(card2, text="Produtos vendidos", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(15,0))
        ctk.CTkLabel(card2, text=f"{qtd_vendida}", font=("Arial", 36, "bold")).pack(anchor="w", padx=20, pady=(0,15))
        
        # Gráficos (Matplotlib)
        graficos_frame = ctk.CTkFrame(self.container_principal, fg_color="white", corner_radius=8, border_width=1, border_color="#d9d9d9")
        graficos_frame.pack(fill="both", expand=True)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
        fig.patch.set_facecolor('white')
        
        if datas:
            ax1.plot(datas, valores_dia, marker='o', color=COR_AZUL)
            ax1.set_title("Vendas por dia (Esse mês)", fontsize=10)
            ax1.grid(True, linestyle='--', alpha=0.5)
        else:
            ax1.text(0.5, 0.5, 'Sem dados', ha='center', va='center')
            
        if nomes_prod:
            ax2.bar(nomes_prod, qtd_prod, color=COR_VERDE)
            ax2.set_title("Produtos mais vendidos", fontsize=10)
            ax2.tick_params(axis='x', rotation=15)
        else:
            ax2.text(0.5, 0.5, 'Sem dados', ha='center', va='center')
            
        plt.tight_layout()
        
        # Cola mágica do Matplotlib [cite: 73]
        canvas = FigureCanvasTkAgg(fig, master=graficos_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_tela_produtos(self):
        self.limpar_container()
        self.atualizar_botoes_nav("Produtos")
        
        frame_tabela = ctk.CTkFrame(self.container_principal, fg_color="white", corner_radius=8, border_width=1, border_color="#d9d9d9")
        frame_tabela.pack(fill="both", expand=True)
        
        ctk.CTkLabel(frame_tabela, text="Lista de produtos", font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=15)
        
        # Treeview para construir a Tabela
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=40, fieldbackground="#f5f5f5", borderwidth=0)
        style.configure("Treeview.Heading", background="#e0e0e0", foreground="black", font=('Arial', 12, 'bold'))
        style.map('Treeview', background=[('selected', COR_AZUL)])
        
        colunas = ("ID", "Nome do produto", "Quantidade no estoque", "Valor de venda")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        self.tree.heading("ID", text="ID do produto")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.heading("Nome do produto", text="Nome do produto")
        self.tree.column("Nome do produto", width=400)
        self.tree.heading("Quantidade no estoque", text="Quantidade no estoque")
        self.tree.column("Quantidade no estoque", width=200, anchor="center")
        self.tree.heading("Valor de venda", text="Valor de venda (R$)")
        self.tree.column("Valor de venda", width=200, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.carregar_produtos_tabela()

    def carregar_produtos_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        produtos = controlador.listar_produtos()
        for p in produtos:
            self.tree.insert("", "end", values=(p[0], p[1], p[2], f"R$ {p[3]:.2f}"))

    # ==================== MODAIS ====================
    def abrir_modal_venda(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Registrar Venda")
        modal.geometry("400x350")
        modal.configure(fg_color=COR_FUNDO)
        modal.transient(self)
        modal.grab_set()
        
        ctk.CTkLabel(modal, text="Registrar venda", font=("Arial", 22, "bold")).pack(pady=25)
        
        produtos = [p[1] for p in controlador.listar_produtos()]
        produtos.insert(0, "Selecione")
        
        ctk.CTkLabel(modal, text="Produto").pack(anchor="w", padx=50)
        combo_produto = ctk.CTkOptionMenu(modal, values=produtos, fg_color="#e0e0e0", text_color="black", button_color="#d6d6d6")
        combo_produto.pack(fill="x", padx=50, pady=(0, 15))
        
        ctk.CTkLabel(modal, text="Quantidade").pack(anchor="w", padx=50)
        entry_qtd = ctk.CTkEntry(modal, placeholder_text="Digite em números a quantidade...", fg_color="#e0e0e0", text_color="black", border_width=0)
        entry_qtd.pack(fill="x", padx=50, pady=(0, 25))
        
        def salvar():
            sucesso, msg = controlador.processar_venda(combo_produto.get(), entry_qtd.get())
            if sucesso:
                modal.destroy()
                self.mostrar_tela_vendas()
            else:
                messagebox.showerror("Erro", msg)
                
        ctk.CTkButton(modal, text="Registrar", fg_color=COR_AZUL, height=40, command=salvar).pack(fill="x", padx=50)

    def abrir_modal_entrada(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Registrar Entrada")
        modal.geometry("400x450")
        modal.configure(fg_color=COR_FUNDO)
        modal.transient(self)
        modal.grab_set()
        
        ctk.CTkLabel(modal, text="Registrar entrada", font=("Arial", 22, "bold")).pack(pady=25)
        
        ctk.CTkLabel(modal, text="Nome do produto").pack(anchor="w", padx=50)
        entry_nome = ctk.CTkEntry(modal, placeholder_text="Digite o nome do produto...", fg_color="#e0e0e0", text_color="black", border_width=0)
        entry_nome.pack(fill="x", padx=50, pady=(0, 15))
        
        ctk.CTkLabel(modal, text="Quantidade").pack(anchor="w", padx=50)
        entry_qtd = ctk.CTkEntry(modal, placeholder_text="Digite em números a quantidade...", fg_color="#e0e0e0", text_color="black", border_width=0)
        entry_qtd.pack(fill="x", padx=50, pady=(0, 15))
        
        ctk.CTkLabel(modal, text="Valor de venda").pack(anchor="w", padx=50)
        entry_valor = ctk.CTkEntry(modal, placeholder_text="Digite o valor em reais...", fg_color="#e0e0e0", text_color="black", border_width=0)
        entry_valor.pack(fill="x", padx=50, pady=(0, 25))
        
        def salvar():
            sucesso, msg = controlador.processar_cadastro(entry_nome.get(), entry_qtd.get(), entry_valor.get())
            if sucesso:
                modal.destroy()
                if hasattr(self, 'tree'):
                    self.carregar_produtos_tabela()
            else:
                messagebox.showerror("Erro", msg)
                
        ctk.CTkButton(modal, text="Registrar", fg_color=COR_AZUL, height=40, command=salvar).pack(fill="x", padx=50)

    def abrir_modal_remover(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Remover Produto")
        modal.geometry("400x250")
        modal.configure(fg_color=COR_FUNDO)
        modal.transient(self)
        modal.grab_set()
        
        ctk.CTkLabel(modal, text="Remover produto", font=("Arial", 22, "bold")).pack(pady=25)
        
        ctk.CTkLabel(modal, text="ID do produto").pack(anchor="w", padx=50)
        entry_id = ctk.CTkEntry(modal, placeholder_text="Digite o ID do produto...", fg_color="#e0e0e0", text_color="black", border_width=0)
        entry_id.pack(fill="x", padx=50, pady=(0, 25))
        
        def confirmar():
            id_txt = entry_id.get()
            if not id_txt:
                messagebox.showerror("Erro", "Insira o ID.")
                return
                
            modal_confirmacao = ctk.CTkToplevel(modal)
            modal_confirmacao.geometry("350x200")
            modal_confirmacao.configure(fg_color=COR_FUNDO)
            modal_confirmacao.transient(modal)
            modal_confirmacao.grab_set()
            
            ctk.CTkLabel(modal_confirmacao, text="Tem certeza que quer\nremover o produto?", font=("Arial", 18, "bold")).pack(pady=25)
            
            def executar_remocao():
                sucesso, msg = controlador.processar_remocao(id_txt)
                if sucesso:
                    modal_confirmacao.destroy()
                    modal.destroy()
                    if hasattr(self, 'tree'):
                        self.carregar_produtos_tabela()
                else:
                    messagebox.showerror("Erro", msg)
                    
            ctk.CTkButton(modal_confirmacao, text="Sim, remover", fg_color=COR_VERMELHA, command=executar_remocao).pack(fill="x", padx=50, pady=(0,10))
            ctk.CTkButton(modal_confirmacao, text="Não, cancelar", fg_color="#e0e0e0", text_color="black", command=modal_confirmacao.destroy).pack(fill="x", padx=50)
            
        ctk.CTkButton(modal, text="Remover", fg_color=COR_VERMELHA, height=40, command=confirmar).pack(fill="x", padx=50)

if __name__ == "__main__":
    app = App()
    app.mainloop()