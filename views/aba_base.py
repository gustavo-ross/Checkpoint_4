import customtkinter as ctk

class AbaBase(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )
        
    def atualizar_dados(self):
        pass