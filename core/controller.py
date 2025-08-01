from core.model import Model
from core.view import View
from core.settings.controller import Controller as SettingsCtrl
from core.stock.controller import Controller as StockCtrl
from core.stock.controller import EntryController as StockEntryCtrl
from core.order.controller import Controller as OrderCtrl

class Controller:
    def __init__(self):
        self.__model = Model()
        self.__view = View(self)

        # instâncias das janelas
        self._settings_ctrl = None
        self._stock_ctrl = None
        self._stock_entry_ctrl = None
        self._order_ctrl = None

    def bootstrap(self):
        self.__view.mainloop()

    def shutdown(self):
        self.__view.destroy()

    def fetch_curr_theme(self):
        return self.__model.fetch_curr_theme()

    def open_settings_window(self):
        if self._settings_ctrl is None or not self._settings_ctrl._view.winfo_exists():
            self._settings_ctrl = SettingsCtrl(master=self.__view, parent=self)
        else: # se já existe, traz para frente
            self._settings_ctrl._view.lift()

    def open_stock_window(self):
        if self._stock_ctrl is None or not self._stock_ctrl._view.winfo_exists():
            self._stock_ctrl = StockCtrl(master=self.__view, parent=self)
        else: # se já existe, traz para frente
            self._stock_ctrl._view.lift()

    def open_stock_entry_window(self):
        if self._stock_entry_ctrl is None or not self._stock_entry_ctrl._view.winfo_exists():
            self._stock_entry_ctrl = StockEntryCtrl(master=self.__view, parent=self)
        else:
            self._stock_entry_ctrl._view.lift()

    def make_stock_report(self):
        return self.__model.make_stock_report()

    def open_order_window(self):
        if self._order_ctrl is None or not self._order_ctrl._view.winfo_exists():
            self._order_ctrl = OrderCtrl(master=self.__view, parent=self)
        else:
            self._order_ctrl._view.lift()

    def make_order_report(self):
        selected_date = self.__view._dialog.date_selected

        return self.__model.make_order_report(selected_date)

    def open_about_window(self):
        pass

    def open_credits_window(self):
        pass