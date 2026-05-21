import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import controlador
from views.aba_base import AbaBase
import config

class AbaProdutos(AbaBase):
    def __init__(self, master):
        super().__init__(master)
        
        self.frame_borda = ctk.CTkFrame(
            self,
            fg_color=config.COR_BRANCO_CARDS,
            corner_radius=8,
            border_width=1,
            border_color=config.COR_CINZA_CLARO
        )
        self.frame_borda.pack(
            fill="both",
            expand=True
        )
        
        self.lbl_titulo = ctk.CTkLabel(
            self.frame_borda,
            text="Lista de produtos",
            font=("Arial", 16, "bold"),
            text_color=config.COR_TEXTO
        )
        self.lbl_titulo.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )
        
        self.frame_pesquisa = ctk.CTkFrame(
            self.frame_borda,
            fg_color="transparent"
        )
        self.frame_pesquisa.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )
        
        self.entry_pesquisa = ctk.CTkEntry(
            self.frame_pesquisa,
            placeholder_text="Pesquisar produto por nome...",
            fg_color=config.COR_CINZA_CLARO,
            border_width=0,
            width=300
        )
        self.entry_pesquisa.pack(
            side="left",
            padx=(0, 10)
        )
        
        self.btn_pesquisar = ctk.CTkButton(
            self.frame_pesquisa,
            text="Buscar",
            fg_color=config.BTN_AZUL_BG,
            hover_color=config.BTN_AZUL_HOVER,
            width=100,
            command=self.realizar_pesquisa
        )
        self.btn_pesquisar.pack(
            side="left",
            padx=(0, 10)
        )
        
        self.btn_limpar = ctk.CTkButton(
            self.frame_pesquisa,
            text="Limpar",
            fg_color=config.BTN_VERMELHA_BG,
            hover_color=config.BTN_VERMELHA_HOVER,
            width=100,
            command=self.limpar_pesquisa
        )
        self.btn_limpar.pack(
            side="left"
        )
        
        self.switch_visao = ctk.CTkSwitch(
            self.frame_pesquisa,
            text="Proporção do Estoque",
            text_color=config.COR_TEXTO,
            command=self.alternar_visao,
            onvalue="grafico",
            offvalue="tabela"
        )
        self.switch_visao.pack(
            side="right"
        )

        self.frame_conteudo = ctk.CTkFrame(
            self.frame_borda,
            fg_color="transparent"
        )
        self.frame_conteudo.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )
        
        colunas = ("ID", "Nome do produto", "Quantidade no estoque", "Valor de venda")
        self.tree = ttk.Treeview(
            self.frame_conteudo,
            columns=colunas,
            show="headings"
        )
        self.tree.heading("ID", text="ID do produto")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.heading("Nome do produto", text="Nome do produto")
        self.tree.column("Nome do produto", width=400)
        self.tree.heading("Quantidade no estoque", text="Quantidade no estoque")
        self.tree.column("Quantidade no estoque", width=200, anchor="center")
        self.tree.heading("Valor de venda", text="Valor de venda (R$)")
        self.tree.column("Valor de venda", width=200, anchor="center")
        
        self.frame_grafico = ctk.CTkFrame(
            self.frame_conteudo,
            fg_color="transparent"
        )

        self.tree.pack(fill="both", expand=True)


    def alternar_visao(self):
        if self.switch_visao.get() == "grafico":
            self.tree.pack_forget()
            self.frame_grafico.pack(fill="both", expand=True)
            self.atualizar_grafico_pizza()
        else:
            self.frame_grafico.pack_forget()
            self.tree.pack(fill="both", expand=True)


    def atualizar_estilo_tabela(self):
        tema = ctk.get_appearance_mode()
        cor_bg = config.COR_BRANCO_CARDS[1] if tema == "Dark" else config.COR_BRANCO_CARDS[0]
        cor_fg = "white" if tema == "Dark" else "black"
        cor_hl = config.COR_CINZA_CLARO[1] if tema == "Dark" else config.COR_CINZA_CLARO[0]

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=cor_bg, foreground=cor_fg, rowheight=40, fieldbackground=cor_bg, borderwidth=0)
        style.configure("Treeview.Heading", background=cor_hl, foreground=cor_fg, font=('Arial', 12, 'bold'))
        style.map('Treeview', background=[('selected', config.COR_AZUL)])


    def atualizar_dados(self, termo=""):
        self.atualizar_estilo_tabela()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if termo:
            produtos = controlador.pesquisar_produtos(termo)
        else:
            produtos = controlador.listar_produtos()
            
        for p in produtos:
            self.tree.insert("", "end", values=(p[0], p[1], p[2], f"R$ {p[3]:.2f}"))
            
        if self.switch_visao.get() == "grafico":
            self.atualizar_grafico_pizza()


    def atualizar_grafico_pizza(self):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        produtos = controlador.listar_produtos()
        nomes = [p[1] for p in produtos if p[2] > 0]
        qtds = [p[2] for p in produtos if p[2] > 0]

        tema_atual = ctk.get_appearance_mode()
        cor_fundo = config.COR_BRANCO_CARDS[1] if tema_atual == "Dark" else config.COR_BRANCO_CARDS[0]
        cor_texto = "white" if tema_atual == "Dark" else "black"

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor(cor_fundo)

        if nomes:
            ax.pie(
                qtds,
                labels=nomes,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'color': cor_texto}
            )
            ax.set_title("Proporção do Estoque Atual", color=cor_texto, pad=20)
        else:
            ax.text(0.5, 0.5, 'Estoque zerado ou vazio', ha='center', va='center', color=cor_texto)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def realizar_pesquisa(self):
        termo = self.entry_pesquisa.get()
        self.atualizar_dados(termo)


    def limpar_pesquisa(self):
        self.entry_pesquisa.delete(0, "end")
        self.atualizar_dados()