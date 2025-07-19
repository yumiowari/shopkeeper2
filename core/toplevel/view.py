import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class View(ttk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Janela Secundária")
        self.geometry("300x150")

        ttk.Label(self, text=self.controller.get_message()).pack(pady=20)
        ttk.Button(self, text="Fechar", command=self.destroy).pack()