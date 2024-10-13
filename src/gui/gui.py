import tkinter as tk
from .pane import Pane
from .directory_tree import DirectoryTree
from .progress_bar import ProgressBar
from .config_pane import ConfigPane
from .list_pane import ListPane
from .action_pane import ActionPane
from tkinter import messagebox
from typing import Tuple, Dict, List, Callable


class Gui:
    """
    Main GUI class that brings together all components.
    """

    def __init__(self, start_function: Callable):
        """
        Initialize the GUI application.

        """

        # Initialised Later
        self._paned_window = None
        self._left_pane = None
        self._directory_tree = None
        self._progress_bar = None
        self._right_pane = None
        self._config_pane = None
        self._list_pane = None
        self._action_pane = None

        # Initialised now
        self._start_function = start_function
        self._root = tk.Tk()
        self._root.title("Topic Modeling")
        self._root.geometry("1000x600")
        self._root.resizable(False, False)
        self.create_panes()

    def create_panes(self):
        """
        Set up the main widgets and layout of the GUI.
        """
        self.create_paned_window()
        self.create_left_pane()
        self.create_right_pane()

    def create_paned_window(self):
        """
        Create the main PanedWindow to split the GUI into left and right sections.
        """
        self._paned_window = tk.PanedWindow(self._root, orient=tk.HORIZONTAL)
        self._paned_window.pack(fill=tk.BOTH, expand=1)

    def create_left_pane(self):
        """
        Create the left pane containing the directory tree and Progress Bar
        """
        self._left_pane = Pane(self._paned_window, padx=5, pady=5)
        self._paned_window.add(self._left_pane.get_frame(), minsize=600)

        self._directory_tree = DirectoryTree(self._left_pane.get_frame(), on_pdf_click=self.on_pdf_click)
        self._progress_bar = ProgressBar(self._left_pane.get_frame())

    def on_pdf_click(self, name: str, path: str):
        """
        Callback function when a PDF is clicked.
        """
        label = name[3:].strip(".pdf")
        self.add_group(label, path)

    def create_right_pane(self):
        """
        Create the right pane, including config pane, list pane, and action pane.
        """
        self._right_pane = Pane(self._paned_window)
        self._paned_window.add(self._right_pane.get_frame(), minsize=400)

        # Top: ConfigPane
        config_inputs = [
            {'label': 'no_below', 'default': 2},
            {'label': 'no_above', 'default': 0.5},
            {'label': 'num_topics', 'default': 20},
            {'label': 'chunk_size', 'default': 1000},
            {'label': "passes", "default": 20},
            {'label': "iterations", "default": 400},
            {'label': 'eval_every', 'default': "None"},
            {'label': 'alpha', 'default': "auto"},
            {'label': 'eta', 'default': "auto"},
            {'label': 'output_dir', 'default': ''}
        ]
        self._config_pane = ConfigPane(self._right_pane.get_frame(), config_inputs, padx=5, pady=5)
        self._config_pane.get_frame().pack(fill=tk.X)

        # Middle: ListPane
        self._list_pane = ListPane(self._right_pane.get_frame(), items=[], paths=[], padx=5, pady=5)
        self._list_pane.get_frame().pack(fill=tk.BOTH, expand=1)
        self._list_pane.listbox.bind("<Key>", self.on_key_press)

        # Bottom: ActionPane
        actions = [
            {'text': 'Start', 'command': self.start_action},
            {'text': 'Clear', 'command': self.clear_list}
        ]
        self._action_pane = ActionPane(self._right_pane.get_frame(), actions, padx=5, pady=5)
        self._action_pane.get_frame().pack(fill=tk.X)

    def on_key_press(self, event):
        if event.keysym == "BackSpace" or event.keysym == "Delete":
            self.delete_group()

    def add_group(self, name: str, path: str):
        """
        Add a new group to the list.
        """
        self._list_pane.add_item(name, path)

    def delete_group(self):
        """
        Delete the selected group.
        """
        selected_item = self._list_pane.get_selected_item()
        if selected_item:
            self._list_pane.delete_selected_item()
        else:
            messagebox.showwarning("Delete Group", "Please select a group to delete.")

    def clear_list(self):
        """
        Clear the list.
        """
        self._list_pane.clear_list()

    def start_action(self):
        """
        Placeholder function for the 'Start' button action.
        """
        self._start_function()

    def get_data(self) -> Tuple[Dict, List[str], Dict]:
        """
        Function to get the data from the GUI

        :return: A tuple of the configuration and file paths
        """
        original_dict = self._config_pane.get_values()
        main_dict = {k: v for k, v in original_dict.items() if k != "output_dir"}
        output_dict = {k: v for k, v in original_dict.items() if k == "output_dir"}
        output_dict["viewing_dir"] = self._directory_tree.get_viewing_directory()
        return main_dict, self._list_pane.get_items(), output_dict

    def run(self):
        """
        Run the main event loop of the Tkinter GUI.
        """
        self._root.mainloop()

    def show_error(self, error: str):
        """
        Function for showing an error message.

        :param error: Error message.
        :return:
        """
        messagebox.showwarning("Error", error)

    def update_bar(self, progress: float):
        if progress < 0:
            self._progress_bar.clear()
        else:
            self._progress_bar.update(progress)


if __name__ == "__main__":
    def start():
        print("Test")
    gui = Gui(start)
    gui.run()
