from core.model import Model
from core.view import View
from core.stock.controller import Controller as StockCtrl
from core.stock.controller import EntryController as StockEntryCtrl
from core.order.controller import Controller as OrderCtrl
from core.order.controller import ProductController as OrderProductCtrl

class Controller:
    def __init__(self):
        self.__model = Model()
        self.__view = View(self)

        # instâncias das janelas
        self.__stock_ctrl = None
        self.__stock_entry_ctrl = None
        self.__order_ctrl = None

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

    def make_stock_report(self):
        return self.__model.make_stock_report()

    def open_order_window(self):
        if self.__order_ctrl is None or not self.__order_ctrl._view.winfo_exists():
            self.__order_ctrl = OrderCtrl(master=self.__view, parent=self)
        else: # se já existe, traz para frente
            self.__order_ctrl._view.lift()

    def make_sales_report(self):
        pass

    def open_about_window(self):
        pass

    def open_credits_window(self):
        pass