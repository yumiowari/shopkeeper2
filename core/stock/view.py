import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class View(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.controller = controller
        self.parent_ctrl = parent_ctrl

        self.title("Inventário")
        self.geometry("400x300")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.parent_ctrl.stock_ctrl = None
        self.destroy()