from core.model import Model
from core.view import View
from core.stock.controller import Controller as StockCtrl

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def run(self):
        self.view.mainloop()

    def open_stock_window(self):
        StockCtrl(master=self.view)