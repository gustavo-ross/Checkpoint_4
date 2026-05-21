import customtkinter as ctk
from tkinter import messagebox
import controlador
from modal_base import ModalBase
import config

class ModalVenda(ModalBase):
    def __init__(self, master, callback):
        super().__init__(
            master,
            titulo="Registrar venda",
            geometria="400x350",
            callback=callback
        )
        
        produtos = [p[1] for p in controlador.listar_produtos()]
        produtos.insert(0, "Selecione")
        
        self.lbl_produto = ctk.CTkLabel(
            self,
            text="Produto"
        )
        self.lbl_produto.pack(
            anchor="w",
            padx=50
        )
        
        self.combo_produto = ctk.CTkOptionMenu(
            self,
            values=produtos,
            fg_color=config.COR_CINZA_CLARO,
            button_color="#d6d6d6"
        )
        self.combo_produto.pack(
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
        sucesso, msg = controlador.processar_venda(
            self.combo_produto.get(),
            self.entry_qtd.get()
        )
        if sucesso:
            self.fechar_com_sucesso()
        else:
            messagebox.showerror(
                "Erro",
                msg
            )