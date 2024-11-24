import customtkinter
import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET
from collections import defaultdict
from PIL import Image, ImageTk

class ItemEditor(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Initialize item storage
        self.items = []
        self.filtered_items = []
        self.grouped_items = defaultdict(list)
        self.current_item_id = None
        self.unsaved_changes = {}
        self.tab_names = {}  # Dictionary to map item IDs to tab names

        # Load and parse the XML file
        self.file_path = "SPEC_WEAPON.xml"
        self.load_item_ids_and_names(self.file_path)

        # Navigation frame
        self.nav_frame = customtkinter.CTkFrame(self, width=300)
        self.nav_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsw")
        self.nav_frame.grid_rowconfigure(1, weight=1)

        # Search bar
        self.search_entry = customtkinter.CTkEntry(self.nav_frame, placeholder_text="Search...")
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.filter_items)

        # Navigation treeview
        style = ttk.Style()
        style.configure("Treeview", background="#222222", foreground="white", fieldbackground="#222222", bordercolor="#222222")
        style.map("Treeview", background=[("selected", "#007acc")], foreground=[("selected", "white")])

        self.nav_tree_frame = customtkinter.CTkFrame(self.nav_frame, fg_color="#222222")
        self.nav_tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.nav_tree_frame.grid_rowconfigure(0, weight=1)
        self.nav_tree_frame.grid_columnconfigure(0, weight=1)

        self.nav_tree = ttk.Treeview(self.nav_tree_frame, show="tree", style="Treeview")
        self.nav_tree.grid(row=0, column=0, sticky="nsew")

        # Load folder icon
        self.folder_icon = ImageTk.PhotoImage(Image.open("assets/icons/folder_icon.png").resize((16, 16)))

        self.populate_nav_tree()

        # Bind treeview selection event
        self.nav_tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # Details frame with tabs
        self.details_frame = customtkinter.CTkFrame(self)
        self.details_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.details_frame.grid_rowconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self.details_frame)
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Set to keep track of open tabs
        self.open_tabs = set()

    def load_item_ids_and_names(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        self.items = [{'ID': item.get('ID'), 'Name': item.get('Name'), 'Kind': item.get('ItemKind3')} for item in root.findall('ItemProp')]
        self.filtered_items = self.items
        self.group_items_by_kind()

    def group_items_by_kind(self):
        self.grouped_items.clear()
        for item in self.items:
            self.grouped_items[item['Kind']].append(item)

    def fetch_item_details(self, item_id):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        item = root.find(f".//ItemProp[@ID='{item_id}']")
        return item

    def populate_nav_tree(self, items=None):
        # Clear the current treeview
        for item in self.nav_tree.get_children():
            self.nav_tree.delete(item)
        # Populate the treeview with grouped items
        items = items or self.filtered_items
        grouped_items = defaultdict(list)
        for item in items:
            grouped_items[item['Kind']].append(item)
        for i, (kind, items) in enumerate(grouped_items.items()):
            group_name = kind.split('_')[-1]  # Strip everything before the GROUPNAME
            parent = self.nav_tree.insert("", "end", text=f"   {group_name}", open=(i == 0), image=self.folder_icon)
            for item in items:
                self.nav_tree.insert(parent, "end", text=item['Name'], values=(item['ID'],))

    def filter_items(self, event):
        # Get the search query
        query = self.search_entry.get().lower()
        # Filter items based on the query
        self.filtered_items = [item for item in self.items if query in item['Name'].lower()]
        # Repopulate the treeview with the filtered items
        self.populate_nav_tree()

    def on_item_select(self, event):
        # Handle item selection from the navigation treeview
        selection = self.nav_tree.selection()
        if selection:
            selected_item_name = self.nav_tree.item(selection[0], "text").strip()
            selected_item = next((item for item in self.items if item['Name'] == selected_item_name), None)
            if selected_item:
                self.open_item_tab(selected_item['ID'], selected_item['Name'])

    def open_item_tab(self, item_id, item_name):
        # Check if there are unsaved changes in the current item
        if self.current_item_id and self.current_item_id in self.unsaved_changes:
            # Open a new tab for the item
            self.create_item_tab(item_id, item_name)
        else:
            # Replace the current item tab
            self.create_item_tab(item_id, item_name, replace=True)

    def create_item_tab(self, item_id, item_name, replace=False):
        # Fetch item details
        item = self.fetch_item_details(item_id)
        if item is None:
            return

        # Remove the current tab if replacing
        if replace and self.current_item_id:
            current_tab_name = self.tab_names.get(self.current_item_id)
            if current_tab_name:
                self.tabview.delete(current_tab_name)
                self.open_tabs.remove(current_tab_name)

        # Create a new tab for the item
        tab = self.tabview.add(item_name)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        # Add search bar for item details at the top
        self.details_search_entry = customtkinter.CTkEntry(tab, placeholder_text="Search properties...")
        self.details_search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Create a canvas and scrollbar for the scrollable frame
        canvas = tk.Canvas(tab, bg="#222222", bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = customtkinter.CTkFrame(canvas, fg_color="#222222")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Enable scrolling when the mouse is over the canvas
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: self._on_mouse_wheel(event, canvas)))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Add item details to the scrollable frame
        row = 0
        col = 0
        for attr, value in item.attrib.items():
            label = customtkinter.CTkLabel(scrollable_frame, text=f"{attr}:")
            label.grid(row=row, column=col, padx=10, pady=5, sticky="e")
            entry = customtkinter.CTkEntry(scrollable_frame)
            entry.insert(0, value)
            entry.grid(row=row, column=col + 1, padx=10, pady=5, sticky="ew")
            entry.bind("<KeyRelease>", lambda e, item_id=item_id: self.mark_unsaved(item_id))
            col += 2
            if col >= 4:
                col = 0
                row += 1

        # Create a frame for the save and close buttons
        button_frame = customtkinter.CTkFrame(tab)
        button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Add save and close buttons to the button frame
        save_button = customtkinter.CTkButton(button_frame, text="Save", command=lambda: self.save_item(item_id))
        save_button.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        close_button = customtkinter.CTkButton(button_frame, text="Close", command=lambda: self.close_item_tab(item_name))
        close_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Bind the search entry to filter item details
        self.details_search_entry.bind("<KeyRelease>", lambda event, frame=scrollable_frame: self.filter_item_details(event, frame))

        # Add the tab to the set of open tabs
        self.open_tabs.add(item_name)
        self.tab_names[item_id] = item_name
        self.current_item_id = item_id

        # Make the new tab the active tab
        self.tabview.set(item_name)

    def mark_unsaved(self, item_id):
        self.unsaved_changes[item_id] = True
        tab_name = self.tab_names.get(item_id)
        if tab_name and not tab_name.endswith(" •"):
            new_tab_name = f"{tab_name} •"
            self.tabview.rename(tab_name, new_tab_name)
            self.tab_names[item_id] = new_tab_name

    def save_item(self, item_id):
        # Fetch the current item details from the tab
        tab_name = self.tab_names.get(item_id)
        if not tab_name:
            return
        tab = self.tabview.tab(tab_name)
        scrollable_frame = tab.winfo_children()[0].winfo_children()[0]
        item_details = {}
        for widget in scrollable_frame.winfo_children():
            if isinstance(widget, customtkinter.CTkEntry):
                attr = widget.grid_info()['row']
                if attr is not None:
                    value = widget.get()
                    item_details[attr] = value

        # Update the XML file with the new item details
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        item = root.find(f".//ItemProp[@ID='{item_id}']")
        if item is not None:
            for attr, value in item_details.items():
                item.set(attr, value)
            tree.write(self.file_path)

        # Remove the unsaved changes marker
        self.unsaved_changes.pop(item_id, None)
        if tab_name.endswith(" •"):
            new_tab_name = tab_name[:-2]
            self.tabview.rename(tab_name, new_tab_name)
            self.tab_names[item_id] = new_tab_name

    def close_item_tab(self, item_name):
        item_id = next((item['ID'] for item in self.items if item['Name'] == item_name), None)
        tab_name = self.tab_names.get(item_id)
        if item_id in self.unsaved_changes:
            response = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save them before closing?")
            if response is None:
                return
            elif response:
                self.save_item(item_id)
            else:
                self.unsaved_changes.pop(item_id, None)
        if tab_name:
            self.tabview.delete(tab_name)
            self.open_tabs.discard(tab_name)
            self.tab_names.pop(item_id, None)
        if self.current_item_id == item_id:
            self.current_item_id = None

    def filter_item_details(self, event, frame):
        query = self.details_search_entry.get().lower()
        print(f"Search query: '{query}'")  # Log the search query

        # Maintain a list of all labels and their corresponding entries
        label_entry_pairs = []
        for widget in frame.winfo_children():
            if isinstance(widget, customtkinter.CTkLabel):
                entry_widget = widget.grid_info()
                row = entry_widget.get('row')
                if row is not None:
                    entry = frame.grid_slaves(row=row, column=entry_widget['column'] + 1)[0]
                    label_entry_pairs.append((widget, entry))

        # Filter the labels and entries based on the search query
        for label, entry in label_entry_pairs:
            label_text = label.cget("text").lower()
            if query in label_text or query == "":
                print(f"Showing: {label_text}")  # Log the label being shown
                label.grid()
                entry.grid()
            else:
                print(f"Hiding: {label_text}")  # Log the label being hidden
                label.grid_remove()
                entry.grid_remove()

        # Additional logging to verify the state of all widgets after filtering
        print("State of all widgets after filtering:")
        for label, entry in label_entry_pairs:
            label_text = label.cget("text").lower()
            print(f"Label: {label_text}, Visible: {label.winfo_ismapped()}, Entry Visible: {entry.winfo_ismapped()}")

        if query == "":
            print("Resetting visibility for all widgets")
            for label, entry in label_entry_pairs:
                label.grid()
                entry.grid()
                print(f"Resetting visibility for: {label.cget('text').lower()}")

    def _on_mouse_wheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")