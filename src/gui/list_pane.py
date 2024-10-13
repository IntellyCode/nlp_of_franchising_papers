from .pane import Pane
import tkinter as tk
from typing import List


class ListPane(Pane):
    """
    Pane that displays a list of items (e.g., groups) with associated paths.

    :param parent: The parent widget.
    :param items: Initial list of items.
    :param **kwargs: Additional keyword arguments for Pane.
    """

    class _Item:
        """
        Private class representing an item with text and path.

        :param text: The text to display in the listbox.
        :param path: The associated path for the item.
        """

        def __init__(self, text: str, path: str, index: int) -> None:
            self.text = text
            self.path = path
            self.index = index

        def __str__(self) -> str:
            # Represent the item by its text for displaying in the listbox
            return str(self.index+1)+". "+self.text

    def __init__(self, parent: tk.Widget, items: List[str], paths: List[str], **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.listbox = tk.Listbox(self.frame, width=150)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        self.items = []  # List of _Item instances
        self.init_items(items, paths)
        self._populate_list()

    def _populate_list(self):
        for item in self.items:
            self.listbox.insert(tk.END, item)

    def init_items(self, items: List[str], paths: List[str]) -> None:
        """
        Populate the listbox with items and paths.

        :param items: List of item texts to display.
        :param paths: List of associated paths for each item.
        :return: None
        """
        for index, text, path in enumerate(zip(items, paths)):
            item = self._Item(text, path, index)
            self.items.append(item)

    def get_selected_item(self) -> str:
        """
        Get the currently selected item's text.

        :return: The selected item's text or an empty string if nothing is selected.
        """
        selected_indices = self.listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            return self.items[index].text
        return ''

    def get_selected_path(self) -> str:
        """
        Get the currently selected item's path.

        :return: The selected item's path or an empty string if nothing is selected.
        """
        selected_indices = self.listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            return self.items[index].path
        return ''

    def add_item(self, text: str, path: str) -> None:
        """
        Add a new item with text and path to the listbox.

        :param text: The item's display text.
        :param path: The associated path for the item.
        :return: None
        """
        # Check for duplicates based on text only
        if text not in [item.text for item in self.items]:

            item = self._Item(text, path,len(self.items))
            self.items.append(item)
            self.listbox.insert(tk.END, item)

    def delete_selected_item(self) -> None:
        """
        Delete the currently selected item from the listbox.

        :return: None
        """
        selected_indices = self.listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            self.listbox.delete(index)
            del self.items[index]
            self.listbox.delete(0, tk.END)
            for index, item in enumerate(self.items):
                item.index = index
            self._populate_list()

    def get_items(self) -> List[tuple]:
        """
        Get all items as a list of (text, path) tuples.

        :return: A list of tuples containing text and path of each item.
        """
        return [(item.text, item.path) for item in self.items]

    def clear_list(self):
        """
        Clear the list
        :return:
        """
        self.listbox.delete(0, tk.END)
        self.items = []
