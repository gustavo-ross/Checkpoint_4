import customtkinter as ctk
import config

class ModalBase(ctk.CTkToplevel):
    def __init__(self, master, titulo="Modal", geometria="400x300", callback=None):
        super().__init__(master)
        
        self.title(titulo)
        self.geometry(geometria)
        self.configure(fg_color=config.COR_FUNDO)
        self.transient(master)
        self.grab_set()
        
        self.callback = callback
        
        self.lbl_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 22, "bold")
        )
        self.lbl_titulo.pack(
            pady=25
        )
        
    def fechar_com_sucesso(self):
        self.destroy()
        if self.callback:
            self.callback()