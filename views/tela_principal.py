import customtkinter as ctk
import controlador
import config
from views.aba_vendas import AbaVendas
from views.aba_produtos import AbaProdutos
from views.aba_historico import AbaHistorico
from views.modal_entrada import ModalEntrada
from views.modal_venda import ModalVenda
from views.modal_remover import ModalRemover
from views.modal_editar import ModalEditar

ctk.set_appearance_mode("Light")

class TelaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestão - ERP SHOW")
        self.geometry("1300x800")
        self.configure(fg_color=config.COR_FUNDO)
        
        controlador.inicializar_sistema()
        
        self.setup_top_header()
        self.setup_header()
        
        self.container_principal = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.container_principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )
        
        self.instancia_aba_vendas = AbaVendas(self.container_principal)
        self.instancia_aba_produtos = AbaProdutos(self.container_principal)
        self.instancia_aba_historico = AbaHistorico(self.container_principal)
        
        self.aba_atual = None
        self.mostrar_aba_vendas()


    def setup_top_header(self):
        self.top_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.top_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 0)
        )
        
        self.lbl_boas_vindas = ctk.CTkLabel(
            self.top_frame,
            text="Bem-vindo(a) ao ERP SHOW",
            font=("Arial", 24, "bold"),
            text_color=config.COR_TEXTO
        )
        self.lbl_boas_vindas.pack(
            side="left"
        )
        
        self.switch_tema = ctk.CTkSwitch(
            self.top_frame,
            text="Modo Escuro",
            command=self.mudar_tema,
            onvalue="Dark",
            offvalue="Light"
        )
        self.switch_tema.pack(
            side="right"
        )


    def mudar_tema(self):
        tema_selecionado = self.switch_tema.get()
        ctk.set_appearance_mode(tema_selecionado)
        self.recarregar_aba_atual()


    def setup_header(self):
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.header_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )
        
        self.nav_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color=config.COR_CINZA_CLARO,
            corner_radius=8
        )
        self.nav_frame.pack(
            side="left"
        )
        
        self.btn_nav_vendas = ctk.CTkButton(
            self.nav_frame,
            text="Vendas",
            fg_color=config.BTN_AZUL_BG,
            hover_color=config.BTN_AZUL_HOVER,
            text_color="white",
            width=120,
            command=self.mostrar_aba_vendas
        )
        self.btn_nav_vendas.pack(
            side="left",
            padx=2,
            pady=2
        )
        
        self.btn_nav_produtos = ctk.CTkButton(
            self.nav_frame,
            text="Produtos",
            fg_color="transparent",
            hover_color=config.BTN_NAV_HOVER,
            text_color=config.COR_TEXTO,
            width=120,
            command=self.mostrar_aba_produtos
        )
        self.btn_nav_produtos.pack(
            side="left",
            padx=2,
            pady=2
        )

        self.btn_nav_historico = ctk.CTkButton(
            self.nav_frame,
            text="Histórico",
            fg_color="transparent",
            hover_color=config.BTN_NAV_HOVER,
            text_color=config.COR_TEXTO,
            width=120,
            command=self.mostrar_aba_historico
        )
        self.btn_nav_historico.pack(
            side="left",
            padx=2,
            pady=2
        )
        
        self.actions_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent"
        )
        self.actions_frame.pack(
            side="right"
        )
        
        self.btn_venda = ctk.CTkButton(
            self.actions_frame,
            text="Registrar venda",
            fg_color=config.BTN_AZUL_BG,
            hover_color=config.BTN_AZUL_HOVER,
            command=lambda: ModalVenda(self, self.recarregar_aba_atual)
        )
        self.btn_venda.pack(
            side="right",
            padx=5
        )
        
        self.btn_entrada = ctk.CTkButton(
            self.actions_frame,
            text="Registrar entrada",
            fg_color=config.BTN_VERDE_BG,
            hover_color=config.BTN_VERDE_HOVER,
            command=lambda: ModalEntrada(self, self.recarregar_aba_atual)
        )
        self.btn_entrada.pack(
            side="right",
            padx=5
        )

        self.btn_editar = ctk.CTkButton(
            self.actions_frame,
            text="Editar produto",
            fg_color=config.BTN_LARANJA_BG,
            hover_color=config.BTN_LARANJA_HOVER,
            command=lambda: ModalEditar(self, self.recarregar_aba_atual)
        )
        self.btn_editar.pack(
            side="right",
            padx=5
        )
        
        self.btn_remover = ctk.CTkButton(
            self.actions_frame,
            text="Remover produto",
            fg_color=config.BTN_VERMELHA_BG,
            hover_color=config.BTN_VERMELHA_HOVER,
            command=lambda: ModalRemover(self, self.recarregar_aba_atual)
        )
        self.btn_remover.pack(
            side="right",
            padx=5
        )


    def esconder_abas(self):
        self.instancia_aba_vendas.pack_forget()
        self.instancia_aba_produtos.pack_forget()
        self.instancia_aba_historico.pack_forget()


    def resetar_botoes_nav(self):
        self.btn_nav_vendas.configure(fg_color="transparent", hover_color=config.BTN_NAV_HOVER, text_color=config.COR_TEXTO)
        self.btn_nav_produtos.configure(fg_color="transparent", hover_color=config.BTN_NAV_HOVER, text_color=config.COR_TEXTO)
        self.btn_nav_historico.configure(fg_color="transparent", hover_color=config.BTN_NAV_HOVER, text_color=config.COR_TEXTO)


    def mostrar_aba_vendas(self):
        self.esconder_abas()
        self.resetar_botoes_nav()
        self.btn_nav_vendas.configure(fg_color=config.BTN_AZUL_BG, hover_color=config.BTN_AZUL_HOVER, text_color="white")
        
        self.aba_atual = self.instancia_aba_vendas
        self.aba_atual.pack(fill="both", expand=True)
        self.aba_atual.atualizar_dados()


    def mostrar_aba_produtos(self):
        self.esconder_abas()
        self.resetar_botoes_nav()
        self.btn_nav_produtos.configure(fg_color=config.BTN_AZUL_BG, hover_color=config.BTN_AZUL_HOVER, text_color="white")
        
        self.aba_atual = self.instancia_aba_produtos
        self.aba_atual.pack(fill="both", expand=True)
        self.aba_atual.atualizar_dados()


    def mostrar_aba_historico(self):
        self.esconder_abas()
        self.resetar_botoes_nav()
        self.btn_nav_historico.configure(fg_color=config.BTN_AZUL_BG, hover_color=config.BTN_AZUL_HOVER, text_color="white")
        
        self.aba_atual = self.instancia_aba_historico
        self.aba_atual.pack(fill="both", expand=True)
        self.aba_atual.atualizar_dados()


    def recarregar_aba_atual(self):
        if self.aba_atual:
            self.aba_atual.atualizar_dados()