import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import controlador
from views.aba_base import AbaBase
import config

class AbaVendas(AbaBase):
    def __init__(self, master):
        super().__init__(master)
        
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=(0, 20))
        
        self.card1 = ctk.CTkFrame(self.cards_frame, fg_color=config.COR_BRANCO_CARDS, corner_radius=8, border_width=1, border_color=config.COR_CINZA_CLARO)
        self.card1.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.lbl_titulo_card1 = ctk.CTkLabel(self.card1, text="Vendas deste mês", font=("Arial", 14), text_color=config.COR_TEXTO)
        self.lbl_titulo_card1.pack(anchor="w", padx=20, pady=(15, 0))
        
        self.lbl_valor_card1 = ctk.CTkLabel(self.card1, text="R$ 0,00", font=("Arial", 36, "bold"), text_color=config.COR_TEXTO)
        self.lbl_valor_card1.pack(anchor="w", padx=20, pady=(0, 15))
        
        self.card2 = ctk.CTkFrame(self.cards_frame, fg_color=config.COR_BRANCO_CARDS, corner_radius=8, border_width=1, border_color=config.COR_CINZA_CLARO)
        self.card2.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        self.lbl_titulo_card2 = ctk.CTkLabel(self.card2, text="Produtos vendidos", font=("Arial", 14), text_color=config.COR_TEXTO)
        self.lbl_titulo_card2.pack(anchor="w", padx=20, pady=(15, 0))
        
        self.lbl_valor_card2 = ctk.CTkLabel(self.card2, text="0", font=("Arial", 36, "bold"), text_color=config.COR_TEXTO)
        self.lbl_valor_card2.pack(anchor="w", padx=20, pady=(0, 15))
        
        self.graficos_frame = ctk.CTkFrame(self, fg_color=config.COR_BRANCO_CARDS, corner_radius=8, border_width=1, border_color=config.COR_CINZA_CLARO)
        self.graficos_frame.pack(fill="x", pady=(0, 20))

        self.frame_borda_tabela = ctk.CTkFrame(
            self,
            fg_color=config.COR_BRANCO_CARDS,
            corner_radius=8,
            border_width=1,
            border_color=config.COR_CINZA_CLARO
        )
        self.frame_borda_tabela.pack(
            fill="both",
            expand=True
        )
        
        self.lbl_titulo_tabela = ctk.CTkLabel(
            self.frame_borda_tabela,
            text="Histórico de Vendas Realizadas",
            font=("Arial", 16, "bold"),
            text_color=config.COR_TEXTO
        )
        self.lbl_titulo_tabela.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )
        
        colunas = ("ID", "Produto", "Quantidade", "Valor Unitário", "Total Pago", "Data")
        self.tree = ttk.Treeview(
            self.frame_borda_tabela,
            columns=colunas,
            show="headings"
        )
        
        self.tree.heading("ID", text="ID Venda")
        self.tree.column("ID", width=80, anchor="center")
        self.tree.heading("Produto", text="Produto")
        self.tree.column("Produto", width=300)
        self.tree.heading("Quantidade", text="Qtd")
        self.tree.column("Quantidade", width=100, anchor="center")
        self.tree.heading("Valor Unitário", text="Valor Unitário")
        self.tree.column("Valor Unitário", width=150, anchor="center")
        self.tree.heading("Total Pago", text="Total Pago")
        self.tree.column("Total Pago", width=150, anchor="center")
        self.tree.heading("Data", text="Data da Venda")
        self.tree.column("Data", width=150, anchor="center")
        
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
        style.map('Treeview', background=[('selected', config.COR_AZUL)])


    def atualizar_dados(self):
        self.atualizar_estilo_tabela()
        faturamento, qtd_vendida, datas, valores_dia, nomes_prod, qtd_prod = controlador.obter_dados_dashboard()
        
        self.lbl_valor_card1.configure(text=f"R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        self.lbl_valor_card2.configure(text=f"{qtd_vendida}")
        
        # Atualiza a Listagem de Vendas na Tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        vendas = controlador.listar_vendas()
        for v in vendas:
            self.tree.insert(
                "",
                "end",
                values=(
                    v[0],
                    v[1],
                    v[2],
                    f"R$ {v[3]:.2f}",
                    f"R$ {v[4]:.2f}",
                    v[5]
                )
            )
        
        # Recarrega os gráficos do Matplotlib
        for widget in self.graficos_frame.winfo_children():
            widget.destroy()
            
        tema_atual = ctk.get_appearance_mode()
        cor_fundo = config.COR_BRANCO_CARDS[1] if tema_atual == "Dark" else config.COR_BRANCO_CARDS[0]
        cor_texto = "white" if tema_atual == "Dark" else "black"
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.2), dpi=100)
        fig.patch.set_facecolor(cor_fundo)
        ax1.set_facecolor(cor_fundo)
        ax2.set_facecolor(cor_fundo)
        ax1.tick_params(colors=cor_texto)
        ax2.tick_params(colors=cor_texto)
        
        for spine in ax1.spines.values(): spine.set_color(cor_texto)
        for spine in ax2.spines.values(): spine.set_color(cor_texto)
        
        if datas:
            ax1.plot(datas, valores_dia, marker='o', color="#1a73e8")
            ax1.set_title("Vendas por dia (Esse mês)", fontsize=10, color=cor_texto)
            ax1.grid(True, linestyle='--', alpha=0.3)
        else:
            ax1.text(0.5, 0.5, 'Sem dados', ha='center', va='center', color=cor_texto)
            
        if nomes_prod:
            ax2.bar(nomes_prod, qtd_prod, color="#0f9d58")
            ax2.set_title("Produtos mais vendidos", fontsize=10, color=cor_texto)
            ax2.tick_params(axis='x', rotation=15)
        else:
            ax2.text(0.5, 0.5, 'Sem dados', ha='center', va='center', color=cor_texto)
            
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.graficos_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)