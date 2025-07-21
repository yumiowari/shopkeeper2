from core.model import Model
from core.view import View
from core.stock.controller import Controller as StockCtrl

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

        # instâncias das janelas
        self.stock_ctrl = None
        self.stock_entry_ctrl = None

    def bootstrap(self):
        self.view.mainloop()

    def shutdown(self):
        self.view.destroy()

    def open_stock_window(self):
        if self.stock_ctrl is None or not self.stock_ctrl.view.winfo_exists():
            self.stock_ctrl = StockCtrl(master=self.view, parent=self)
        else: # se já existe, traz para frente
            self.stock_ctrl.view.lift()

    def open_stock_entry_window(self):
        pass