import tkinter as tk
from pane import Pane
from directory_tree import DirectoryTree
from config_pane import ConfigPane
from list_pane import ListPane
from action_pane import ActionPane
from tkinter import messagebox


class Gui:
    """
    Main GUI class that brings together all components.
    """

    def __init__(self) -> None:
        """
        Initialize the GUI application.

        :return: None
        """

        self.root = tk.Tk()
        self.root.title("Topic Modeling")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.create_widgets()
        self.run()


    def create_widgets(self) -> None:
        """
        Set up the main widgets and layout of the GUI.

        :return: None
        """
        self.create_paned_window()
        self.create_left_pane()
        self.create_right_pane()

    def create_paned_window(self) -> None:
        """
        Create the main PanedWindow to split the GUI into left and right sections.

        :return: None
        """
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

    def create_left_pane(self) -> None:
        """
        Create the left pane containing the directory tree.

        :return: None
        """
        self.left_pane = Pane(self.paned_window,padx=5, pady=5)
        self.paned_window.add(self.left_pane.get_frame(), minsize=600)
        self.directory_tree = DirectoryTree(self.left_pane.get_frame(), on_pdf_click=self.on_pdf_click)

    def on_pdf_click(self, name: str, path:str) -> None:
        """
        Callback function when a PDF is clicked.

        :return: None
        """
        label = name[3:].strip(".pdf")
        self.add_group(label, path)


    def create_right_pane(self) -> None:
        """
        Create the right pane, including config pane, list pane, and action pane.

        :return: None
        """
        self.right_pane = Pane(self.paned_window)
        self.paned_window.add(self.right_pane.get_frame(),minsize=400)

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
        ]
        self.config_pane = ConfigPane(self.right_pane.get_frame(), config_inputs, padx=5, pady=5)
        self.config_pane.get_frame().pack(fill=tk.X)

        # Middle: ListPane
        self.list_pane = ListPane(self.right_pane.get_frame(), items=[],paths=[], padx=5, pady=5)
        self.list_pane.get_frame().pack(fill=tk.BOTH, expand=1)
        self.list_pane.listbox.bind("<Key>", self.on_key_press)

        # Bottom: ActionPane
        actions = [
            {'text': 'Start', 'command': self.start_action}
        ]
        self.action_pane = ActionPane(self.right_pane.get_frame(), actions, padx=5, pady=5)
        self.action_pane.get_frame().pack(fill=tk.X)

    def on_key_press(self, event):
        if event.keysym == "BackSpace" or event.keysym == "Delete":
            self.delete_group()

    def add_group(self, name: str, path: str) -> None:
        """
        Add a new group to the list.

        :return: None
        """
        self.list_pane.add_item(name, path)

    def delete_group(self) -> None:
        """
        Delete the selected group.

        :return: None
        """
        selected_item = self.list_pane.get_selected_item()
        if selected_item:
            self.list_pane.delete_selected_item()
        else:
            messagebox.showwarning("Delete Group", "Please select a group to delete.")

    def start_action(self) -> None:
        """
        Placeholder function for the 'Start' button action.

        :return: None
        """
        messagebox.showinfo("Values", f"Config Values: \n {self.config_pane.get_values()}\n Files: \n {self.list_pane.get_items()}")

    def run(self) -> None:
        """
        Run the main event loop of the Tkinter GUI.

        :return: None
        """
        self.root.mainloop()

    def show_error(self, error: str):
        """
        Function for showing an error message.

        :param error: Error message.
        :return:
        """
        messagebox.showwarning("Error", error)


if __name__ == "__main__":
    gui = Gui()
