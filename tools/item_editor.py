import customtkinter
import tkinter as tk

# Set the dark theme for customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class ItemEditor(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Navigation frame
        self.nav_frame = customtkinter.CTkFrame(self, width=300)
        self.nav_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsw")
        self.nav_frame.grid_rowconfigure(1, weight=1)

        # Search bar
        self.search_entry = customtkinter.CTkEntry(self.nav_frame, placeholder_text="Search...")
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.filter_items)

        # Navigation list (dummy data)
        self.nav_listbox = tk.Listbox(self.nav_frame, bg="#1e1e1e", fg="white", selectbackground="#007acc", selectforeground="white")
        self.nav_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.items = ["Sword", "Shield", "Helmet", "Armor", "Boots"]  # Store all items
        self.populate_nav_listbox()

        # Details frame with tabs
        self.details_frame = customtkinter.CTkFrame(self)
        self.details_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.details_frame.grid_rowconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self.details_frame)
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Set to keep track of open tabs
        self.open_tabs = set()

        # Bind listbox selection event
        self.nav_listbox.bind("<<ListboxSelect>>", self.on_item_select)

    def populate_nav_listbox(self, items=None):
        # Clear the current listbox
        self.nav_listbox.delete(0, tk.END)
        # Populate the listbox with items
        items = items or self.items
        for item in items:
            self.nav_listbox.insert("end", item)

    def filter_items(self, event):
        # Get the search query
        query = self.search_entry.get().lower()
        # Filter items based on the query
        filtered_items = [item for item in self.items if query in item.lower()]
        # Repopulate the listbox with the filtered items
        self.populate_nav_listbox(filtered_items)

    def on_item_select(self, event):
        # Handle item selection from the navigation list
        selection = self.nav_listbox.curselection()
        if selection:
            selected_item = self.nav_listbox.get(selection)
            self.open_item_tab(selected_item)

    def open_item_tab(self, item_name):
        # Check if the tab already exists
        if item_name in self.open_tabs:
            # If the tab is already open, do nothing
            return
        else:
            # Create a new tab for the item
            tab = self.tabview.add(item_name)
            tab.grid_rowconfigure(0, weight=0)
            tab.grid_columnconfigure(0, weight=1)

            # Add item details to the tab
            item_details_label = customtkinter.CTkLabel(tab, text=f"Details for {item_name}")
            item_details_label.grid(row=0, column=0, padx=20, pady=20)

            # Add a close button to the tab header
            close_button = customtkinter.CTkButton(tab, text="Close", command=lambda: self.close_item_tab(item_name))
            close_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

            # Add the tab to the set of open tabs
            self.open_tabs.add(item_name)

            # Make the new tab the active tab
            self.tabview.set(item_name)

    def close_item_tab(self, item_name):
        self.tabview.delete(item_name)
        self.open_tabs.remove(item_name)