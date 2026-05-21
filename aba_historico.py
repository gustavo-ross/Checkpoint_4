import customtkinter as ctk
from tkinter import ttk
import controlador
from aba_base import AbaBase
import config

class AbaHistorico(AbaBase):
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
            text="Histórico de alterações de preço",
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
            placeholder_text="Pesquisar histórico por produto...",
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
        
        colunas = ("ID", "Produto", "Valor Antigo", "Valor Novo", "Data da Alteração")
        self.tree = ttk.Treeview(
            self.frame_borda,
            columns=colunas,
            show="headings"
        )
        
        self.tree.heading("ID", text="ID Registro")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.heading("Produto", text="Produto Modificado")
        self.tree.column("Produto", width=300)
        self.tree.heading("Valor Antigo", text="Valor Antigo")
        self.tree.column("Valor Antigo", width=150, anchor="center")
        self.tree.heading("Valor Novo", text="Valor Novo")
        self.tree.column("Valor Novo", width=150, anchor="center")
        self.tree.heading("Data da Alteração", text="Data da Alteração")
        self.tree.column("Data da Alteração", width=200, anchor="center")
        
        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    def atualizar_estilo_tabela(self):
        tema = ctk.get_appearance_mode()
        cor_bg = config.COR_BRANCO_CARDS[1] if tema == "Dark" else config.COR_BRANCO_CARDS[0]
        cor_fg = "white" if tema == "Dark" else "black"
        cor_hl = config.COR_CINZA_CLARO[1] if tema == "Dark" else config.COR_CINZA_CLARO[0]

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=cor_bg, foreground=cor_fg, rowheight=40, fieldbackground=cor_bg, borderwidth=0)
        style.configure("Treeview.Heading", background=cor_hl, foreground=cor_fg, font=('Arial', 12, 'bold'))

    def atualizar_dados(self, termo=""):
        self.atualizar_estilo_tabela()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if termo:
            historico = controlador.pesquisar_historico(termo)
        else:
            historico = controlador.listar_historico()
            
        for h in historico:
            self.tree.insert("", "end", values=(h[0], h[1], f"R$ {h[2]:.2f}", f"R$ {h[3]:.2f}", h[4]))

    def realizar_pesquisa(self):
        termo = self.entry_pesquisa.get()
        self.atualizar_dados(termo)

    def limpar_pesquisa(self):
        self.entry_pesquisa.delete(0, "end")
        self.atualizar_dados()