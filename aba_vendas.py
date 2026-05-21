import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import controlador
from aba_base import AbaBase
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
        self.graficos_frame.pack(fill="both", expand=True)

    def atualizar_dados(self):
        faturamento, qtd_vendida, datas, valores_dia, nomes_prod, qtd_prod = controlador.obter_dados_dashboard()
        
        self.lbl_valor_card1.configure(text=f"R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        self.lbl_valor_card2.configure(text=f"{qtd_vendida}")
        
        for widget in self.graficos_frame.winfo_children():
            widget.destroy()
            
        tema_atual = ctk.get_appearance_mode()
        cor_fundo = config.COR_BRANCO_CARDS[1] if tema_atual == "Dark" else config.COR_BRANCO_CARDS[0]
        cor_texto = "white" if tema_atual == "Dark" else "black"
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
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