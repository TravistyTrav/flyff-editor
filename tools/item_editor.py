import customtkinter

class ItemEditor(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = customtkinter.CTkLabel(self, text="Item Editor")
        self.label.grid(row=0, column=0, padx=20, pady=20)