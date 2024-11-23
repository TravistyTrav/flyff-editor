import customtkinter

class MainNavigation(customtkinter.CTkFrame):
    def __init__(self, master, switch_frame, **kwargs):
        super().__init__(master, **kwargs)
        self.switch_frame = switch_frame

        self.label = customtkinter.CTkLabel(self, text="Main Navigation")
        self.label.grid(row=0, column=0, padx=20)

        self.item_editor_button = customtkinter.CTkButton(self, text="Item Editor", command=lambda: self.switch_frame("ItemEditor"))
        self.item_editor_button.grid(row=1, column=0, padx=20, pady=10)

        self.other_editor_button = customtkinter.CTkButton(self, text="Other Editor", command=lambda: self.switch_frame("OtherEditor"))
        self.other_editor_button.grid(row=2, column=0, padx=20, pady=10)