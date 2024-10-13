import os
import tkinter as tk
from tkinter import ttk
from typing import Any, Optional


class DirectoryTree:
    """
    Class to handle directory data and display it, including navigation and PDF files.

    :param parent: The parent widget.
    :param on_pdf_click: Callback function when a PDF is clicked.
    """

    def __init__(self, parent: tk.Widget, on_pdf_click):
        # Initialised later
        self._contents_frame = None
        self._scrollbar = None
        self._contents_listbox = None

        # Initialised here
        self._parent = parent
        self._current_path = os.path.expanduser('~')
        self._on_pdf_click = on_pdf_click

        self._path_frame = tk.Frame(self._parent)
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        """
        Create the widgets for the directory tree display.
        """
        self._path_frame.pack(fill=tk.X)

        # Separator
        separator = ttk.Separator(self._parent, orient='horizontal')
        separator.pack(fill=tk.X, pady=5)

        # Frame for the directory contents
        self._contents_frame = tk.Frame(self._parent)
        self._contents_frame.pack(fill=tk.BOTH, expand=1)

        # Scrollbar for the contents list
        self._scrollbar = tk.Scrollbar(self._contents_frame)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox to display folders and PDF files
        self._contents_listbox = tk.Listbox(self._contents_frame, yscrollcommand=self._scrollbar.set)
        self._contents_listbox.pack(fill=tk.BOTH, expand=1)
        self._scrollbar.config(command=self._contents_listbox.yview)

        # Bind double-click event
        self._contents_listbox.bind('<Double-Button-1>', self.on_item_double_click)
        self._contents_listbox.bind("<Return>", self.on_item_double_click)

    def update_display(self):
        """
        Update the display with the current path and contents.
        """
        # Clear previous path buttons
        for widget in self._path_frame.winfo_children():
            widget.destroy()

        # Display the current path with clickable components
        path_parts = self._current_path.strip(os.sep).split(os.sep)
        btn = tk.Button(self._path_frame, text="~", command=lambda p=os.path.expanduser('~'): self.navigate_to(p))
        btn.pack(side=tk.LEFT)
        tk.Label(self._path_frame, text=":").pack(side=tk.LEFT)
        accumulated_path = os.sep if self._current_path.startswith(os.sep) else ''
        for index, part in enumerate(path_parts):
            accumulated_path = os.path.join(accumulated_path, part)
            if len(path_parts) - index < 3:
                btn = tk.Button(self._path_frame, text=part or os.sep, command=lambda p=accumulated_path: self.navigate_to(p))
                btn.pack(side=tk.LEFT)
                btn.update_idletasks()
                if index < len(path_parts) - 1:
                    label = tk.Label(self._path_frame, text=os.sep)
                    label.pack(side=tk.LEFT)
                    label.update_idletasks()
        self.populate_contents()

    def populate_contents(self):
        """
        Populate the listbox with folders and PDF files in the current directory.
        """
        # Clear the listbox
        self._contents_listbox.delete(0, tk.END)
        try:
            items = os.listdir(self._current_path)
            items.sort()
            for item in items:
                if item.startswith('.'):
                    continue
                abs_path = os.path.join(self._current_path, item)
                if os.path.isdir(abs_path):
                    display_text = f" > {item}"
                    self._contents_listbox.insert(tk.END, display_text)
                elif item.lower().endswith('.pdf'):
                    display_text = f" - {item}"
                    self._contents_listbox.insert(tk.END, display_text)
        except PermissionError:
            self._contents_listbox.insert(tk.END, "Permission Denied")

    def navigate_to(self, path: str) -> None:
        """
        Navigate to the specified directory and update the display.

        :param path: The path to navigate to.
        :return: None
        """
        if os.path.isdir(path):
            self._current_path = path
            self.update_display()

    def on_item_double_click(self, event: Any):
        """
        Event handler for double-clicking an item in the contents list.
        """
        selection = self._contents_listbox.curselection()
        if selection:
            index = selection[0]
            item_text = self._contents_listbox.get(index)
            item_name = item_text[3:]
            abs_path = os.path.join(self._current_path, item_name)
            if item_text.endswith('.pdf'):
                if self._on_pdf_click:
                    self._on_pdf_click(item_text, abs_path)
                else:
                    pass
            else:
                self.navigate_to(abs_path)

    def get_widget(self) -> tk.Widget:
        """
        Get the parent widget containing the directory tree display.

        :return: The parent widget.
        """
        return self._parent

    def get_viewing_directory(self) -> str:
        return self._current_path
