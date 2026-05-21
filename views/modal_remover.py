import customtkinter as ctk
from tkinter import messagebox
import controlador
from views.modal_base import ModalBase
import config

class ModalRemover(ModalBase):
    def __init__(self, master, callback):
        super().__init__(
            master,
            titulo="Remover produto",
            geometria="400x250",
            callback=callback
        )
        
        self.lbl_id = ctk.CTkLabel(
            self,
            text="ID do produto"
        )
        self.lbl_id.pack(
            anchor="w",
            padx=50
        )
        
        self.entry_id = ctk.CTkEntry(
            self,
            placeholder_text="Digite o ID do produto...",
            fg_color=config.COR_CINZA_CLARO,
            border_width=0
        )
        self.entry_id.pack(
            fill="x",
            padx=50,
            pady=(0, 25)
        )
        
        self.btn_remover = ctk.CTkButton(
            self,
            text="Remover",
            fg_color=config.BTN_VERMELHA_BG,
            hover_color=config.BTN_VERMELHA_HOVER,
            height=40,
            command=self.confirmar
        )
        self.btn_remover.pack(
            fill="x",
            padx=50
        )


    def confirmar(self):
        id_txt = self.entry_id.get()
        if not id_txt:
            messagebox.showerror(
                "Erro",
                "Insira o ID."
            )
            return
            
        self.modal_confirmacao = ctk.CTkToplevel(self)
        self.modal_confirmacao.geometry("350x200")
        self.modal_confirmacao.configure(fg_color=config.COR_FUNDO)
        self.modal_confirmacao.transient(self)
        self.modal_confirmacao.grab_set()
        
        self.lbl_certeza = ctk.CTkLabel(
            self.modal_confirmacao,
            text="Tem certeza que quer\nremover o produto?",
            font=("Arial", 18, "bold")
        )
        self.lbl_certeza.pack(
            pady=25
        )
        

        def executar_remocao():
            sucesso, msg = controlador.processar_remocao(id_txt)
            if sucesso:
                self.modal_confirmacao.destroy()
                self.fechar_com_sucesso()
            else:
                messagebox.showerror(
                    "Erro",
                    msg
                )
                
        self.btn_sim = ctk.CTkButton(
            self.modal_confirmacao,
            text="Sim, remover",
            fg_color=config.BTN_VERMELHA_BG,
            hover_color=config.BTN_VERMELHA_HOVER,
            command=executar_remocao
        )
        self.btn_sim.pack(
            fill="x",
            padx=50,
            pady=(0, 10)
        )
        
        self.btn_nao = ctk.CTkButton(
            self.modal_confirmacao,
            text="Não, cancelar",
            fg_color=config.COR_CINZA_CLARO,
            hover_color=config.BTN_NAV_HOVER,
            text_color=config.COR_TEXTO,
            command=self.modal_confirmacao.destroy
        )
        self.btn_nao.pack(
            fill="x",
            padx=50
        )