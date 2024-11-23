import customtkinter
from assets.icons.icons import item_editor_icon_ctk, cog_icon_ctk, info_icon_ctk

class MainNavigation(customtkinter.CTkFrame):
    def __init__(self, master, switch_frame, **kwargs):
        super().__init__(master, **kwargs)
        self.switch_frame = switch_frame

        # Configure grid rows
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=0)

        self.label = customtkinter.CTkLabel(self, text="Main Navigation")
        self.label.grid(row=0, column=0, padx=20, pady=10)

        self.item_editor_button = customtkinter.CTkButton(self, text="Item Editor", image=item_editor_icon_ctk, command=lambda: self.switch_frame("ItemEditor"))
        self.item_editor_button.grid(row=1, column=0, padx=20, pady=10)

        self.other_editor_button = customtkinter.CTkButton(self, text="Other Editor", command=lambda: self.switch_frame("OtherEditor"))
        self.other_editor_button.grid(row=2, column=0, padx=20, pady=10)

        # Spacer row to push bottom buttons to the bottom
        self.spacer = customtkinter.CTkLabel(self, text="")
        self.spacer.grid(row=3, column=0, padx=20, pady=10)

        self.bottom_button1 = customtkinter.CTkButton(self, text="Information", image=info_icon_ctk, command=lambda: self.switch_frame("Bottom1"))
        self.bottom_button1.grid(row=4, column=0, padx=20, pady=10, sticky="s")

        self.bottom_button2 = customtkinter.CTkButton(self, text="Settings", image=cog_icon_ctk, command=lambda: self.switch_frame("Bottom2"))
        self.bottom_button2.grid(row=5, column=0, padx=20, pady=10, sticky="s")

        self.bottom_button3 = customtkinter.CTkButton(self, text="Github", command=lambda: self.switch_frame("Bottom3"))
        self.bottom_button3.grid(row=6, column=0, padx=20, pady=10, sticky="s")