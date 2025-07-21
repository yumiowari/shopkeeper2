import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class View(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl

        self.title("Inventário")
        self.geometry("600x450")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.__notebook = ttk.Notebook(self)

        # CREATE
        self.__create_frame = ttk.Frame(self.__notebook)

        # READ (CONFER)
        self.__confer_frame = ttk.Frame(self.__notebook)

        # UPDATE
        self.__update_frame = ttk.Frame(self.__notebook)

        # DELETE
        self.__delete_frame = ttk.Frame(self.__notebook)

        self.__notebook.add(self.__create_frame, text="Cadastrar")
        self.__notebook.add(self.__confer_frame, text="Consultar")
        self.__notebook.add(self.__update_frame, text="Atualizar")
        self.__notebook.add(self.__delete_frame, text="Remover")

        self.__notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def on_close(self):
        self.__parent_ctrl.stock_ctrl = None
        self.destroy()