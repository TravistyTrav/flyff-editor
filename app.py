import customtkinter
from navigation import MainNavigation
from tools.item_editor import ItemEditor
from tools.other_editor import OtherEditor

customtkinter.set_default_color_theme("assets/themes/zennr-theme.json")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.minsize(1280, 720)
        self.title("Zennr - Flyff Editor")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.main_navigation = MainNavigation(master=self, switch_frame=self.switch_frame)
        self.main_navigation.grid(row=0, column=0, padx=0, pady=0, sticky="nsw")

        self.current_frame = None
        self.switch_frame("ItemEditor")

    def switch_frame(self, frame_name):
        new_frame = None
        if frame_name == "ItemEditor":
            new_frame = ItemEditor(master=self)
        elif frame_name == "OtherEditor":
            new_frame = OtherEditor(master=self)

        if self.current_frame is not None:
            self.current_frame.grid_forget()
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")