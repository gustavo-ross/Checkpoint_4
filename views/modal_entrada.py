import customtkinter as ctk
from tkinter import messagebox
import controlador
from views.modal_base import ModalBase
import config

class ModalEntrada(ModalBase):
    def __init__(self, master, callback):
        super().__init__(
            master,
            titulo="Registrar entrada",
            geometria="400x450",
            callback=callback
        )
        
        self.lbl_nome = ctk.CTkLabel(
            self,
            text="Nome do produto"
        )
        self.lbl_nome.pack(
            anchor="w",
            padx=50
        )
        
        self.entry_nome = ctk.CTkEntry(
            self,
            placeholder_text="Digite o nome do produto...",
            fg_color=config.COR_CINZA_CLARO,
            border_width=0
        )
        self.entry_nome.pack(
            fill="x",
            padx=50,
            pady=(0, 15)
        )
        
        self.lbl_qtd = ctk.CTkLabel(
            self,
            text="Quantidade"
        )
        self.lbl_qtd.pack(
            anchor="w",
            padx=50
        )
        
        self.entry_qtd = ctk.CTkEntry(
            self,
            placeholder_text="Digite em números a quantidade...",
            fg_color=config.COR_CINZA_CLARO,
            border_width=0
        )
        self.entry_qtd.pack(
            fill="x",
            padx=50,
            pady=(0, 15)
        )
        
        self.lbl_valor = ctk.CTkLabel(
            self,
            text="Valor de venda"
        )
        self.lbl_valor.pack(
            anchor="w",
            padx=50
        )
        
        self.entry_valor = ctk.CTkEntry(
            self,
            placeholder_text="Digite o valor em reais...",
            fg_color=config.COR_CINZA_CLARO,
            border_width=0
        )
        self.entry_valor.pack(
            fill="x",
            padx=50,
            pady=(0, 25)
        )
        
        self.btn_registrar = ctk.CTkButton(
            self,
            text="Registrar",
            fg_color=config.BTN_AZUL_BG,
            hover_color=config.BTN_AZUL_HOVER,
            height=40,
            command=self.salvar
        )
        self.btn_registrar.pack(
            fill="x",
            padx=50
        )

    def salvar(self):
        sucesso, msg = controlador.processar_cadastro(
            self.entry_nome.get(),
            self.entry_qtd.get(),
            self.entry_valor.get()
        )
        if sucesso:
            self.fechar_com_sucesso()
        else:
            messagebox.showerror(
                "Erro",
                msg
            )