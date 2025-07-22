from core.model import Model
from core.view import View
from core.stock.controller import Controller as StockCtrl
from core.stock.controller import EntryController as StockEntryCtrl

class Controller:
    def __init__(self):
        self.__model = Model()
        self.__view = View(self)

        # instâncias das janelas
        self.__stock_ctrl = None
        self.__stock_entry_ctrl = None

    def bootstrap(self):
        self.__view.mainloop()

    def shutdown(self):
        self.__view.destroy()

    def open_stock_window(self):
        if self.__stock_ctrl is None or not self.__stock_ctrl._view.winfo_exists():
            self.__stock_ctrl = StockCtrl(master=self.__view, parent=self)
        else: # se já existe, traz para frente
            self.__stock_ctrl._view.lift()

    def open_stock_entry_window(self):
        if self.__stock_entry_ctrl is None or not self.__stock_entry_ctrl._view.winfo_exists():
            self.__stock_entry_ctrl = StockEntryCtrl(master=self.__view, parent=self)
        else: # se já existe, traz para frente
            self.__stock_entry_ctrl._view.lift()