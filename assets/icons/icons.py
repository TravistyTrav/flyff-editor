from PIL import Image
import customtkinter

# Convert images to CTkImage
item_editor_icon_ctk = customtkinter.CTkImage(Image.open("assets/icons/edit_icon_white.png"), size=(15, 15))
cog_icon_ctk = customtkinter.CTkImage(Image.open("assets/icons/cog_icon_white.png"), size=(15, 15))
info_icon_ctk = customtkinter.CTkImage(Image.open("assets/icons/info_icon_white.png"), size=(15, 15))