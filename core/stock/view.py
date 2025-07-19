import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class View(ttk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Inventário")
        self.geometry("400x300")