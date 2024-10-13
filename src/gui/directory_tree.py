import os
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Optional


class DirectoryTree:
    """
    Class to handle directory data and display it, including navigation and PDF files.

    :param parent: The parent widget.
    :param on_pdf_click: Callback function when a PDF is clicked.
    """

    def __init__(self, parent: tk.Widget, on_pdf_click) -> None:
        self.parent = parent
        self.current_path = os.path.expanduser('~')
        self.on_pdf_click = on_pdf_click

        self.path_frame = tk.Frame(self.parent)
        self.create_widgets()
        self.update_display()

    def create_widgets(self) -> None:
        """
        Create the widgets for the directory tree display.

        :return: None
        """
        self.path_frame.pack(fill=tk.X)

        # Separator
        separator = ttk.Separator(self.parent, orient='horizontal')
        separator.pack(fill=tk.X, pady=5)

        # Frame for the directory contents
        self.contents_frame = tk.Frame(self.parent)
        self.contents_frame.pack(fill=tk.BOTH, expand=1)

        # Scrollbar for the contents list
        self.scrollbar = tk.Scrollbar(self.contents_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox to display folders and PDF files
        self.contents_listbox = tk.Listbox(self.contents_frame, yscrollcommand=self.scrollbar.set)
        self.contents_listbox.pack(fill=tk.BOTH, expand=1)
        self.scrollbar.config(command=self.contents_listbox.yview)

        # Bind double-click event
        self.contents_listbox.bind('<Double-Button-1>', self.on_item_double_click)

    def update_display(self) -> None:
        """
        Update the display with the current path and contents.

        :return: None
        """
        # Clear previous path buttons
        for widget in self.path_frame.winfo_children():
            widget.destroy()

        # Display the current path with clickable components
        path_parts = self.current_path.strip(os.sep).split(os.sep)
        btn = tk.Button(self.path_frame, text="~", command=lambda p=os.path.expanduser('~'): self.navigate_to(p))
        btn.pack(side=tk.LEFT)
        tk.Label(self.path_frame, text=":").pack(side=tk.LEFT)
        accumulated_path = os.sep if self.current_path.startswith(os.sep) else ''
        for index, part in enumerate(path_parts):
            accumulated_path = os.path.join(accumulated_path, part)
            if len(path_parts) - index < 3:
                btn = tk.Button(self.path_frame, text=part or os.sep, command=lambda p=accumulated_path: self.navigate_to(p))
                btn.pack(side=tk.LEFT)
                btn.update_idletasks()
                if index < len(path_parts) - 1:
                    label = tk.Label(self.path_frame, text=os.sep)
                    label.pack(side=tk.LEFT)
                    label.update_idletasks()
        self.populate_contents()

    def populate_contents(self) -> None:
        """
        Populate the listbox with folders and PDF files in the current directory.

        :return: None
        """
        # Clear the listbox
        self.contents_listbox.delete(0, tk.END)
        try:
            items = os.listdir(self.current_path)
            items.sort()
            for item in items:
                if item.startswith('.'):
                    continue
                abs_path = os.path.join(self.current_path, item)
                if os.path.isdir(abs_path):
                    display_text = f" > {item}"
                    self.contents_listbox.insert(tk.END, display_text)
                elif item.lower().endswith('.pdf'):
                    display_text = f" - {item}"
                    self.contents_listbox.insert(tk.END, display_text)
        except PermissionError:
            self.contents_listbox.insert(tk.END, "Permission Denied")

    def navigate_to(self, path: str) -> None:
        """
        Navigate to the specified directory and update the display.

        :param path: The path to navigate to.
        :return: None
        """
        if os.path.isdir(path):
            self.current_path = path
            self.update_display()

    def on_item_double_click(self, event: Any) -> None:
        """
        Event handler for double-clicking an item in the contents list.

        :param event: The Tkinter event object.
        :return: None
        """
        selection = self.contents_listbox.curselection()
        if selection:
            index = selection[0]
            item_text = self.contents_listbox.get(index)
            item_name = item_text[3:]
            abs_path = os.path.join(self.current_path, item_name)
            if item_text.endswith('.pdf'):
                if self.on_pdf_click:
                    self.on_pdf_click(item_text, abs_path)
                else:
                    tk.messagebox.showinfo("PDF Clicked", "PDF Clicked")
            else:
                self.navigate_to(abs_path)

    def get_widget(self) -> tk.Widget:
        """
        Get the parent widget containing the directory tree display.

        :return: The parent widget.
        """
        return self.parent
