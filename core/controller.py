from core.model import Model as MainModel
from core.view import View as MainView
from core.settings.controller import Controller as SettingsCtrl
from core.stock.controller import CRUDController as StockCtrl
from core.stock.controller import EntryController as StockEntryCtrl
from core.order.controller import CreateOrderController as CreateOrderCtrl
from core.order.controller import ConferOrderController as ConferOrderCtrl

class Controller:
    def __init__(self):
        self.__model = MainModel()
        self.__view = MainView(self)

        # instâncias das janelas
        self._settings_ctrl = None
        self._stock_ctrl = None
        self._stock_entry_ctrl = None
        self._create_order_ctrl = None
        self._confer_order_ctrl = None

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
        else:
            self._stock_ctrl._view.lift()

    def open_stock_entry_window(self):
        if self._stock_entry_ctrl is None or not self._stock_entry_ctrl._view.winfo_exists():
            self._stock_entry_ctrl = StockEntryCtrl(master=self.__view, parent=self)
        else:
            self._stock_entry_ctrl._view.lift()

    def make_stock_report(self):
        return self.__model.make_stock_report()

    def open_create_order_window(self):
        if self._create_order_ctrl is None or not self._create_order_ctrl._view.winfo_exists():
            self._create_order_ctrl = CreateOrderCtrl(master=self.__view, parent=self)
        else:
            self._create_order_ctrl._view.lift()

    def open_confer_order_window(self):
        if self._confer_order_ctrl is None or not self._confer_order_ctrl._view.winfo_exists():
            self._confer_order_ctrl = ConferOrderCtrl(master=self.__view, parent=self)
        else:
            self._confer_order_ctrl._view.lift()

    def make_order_report(self):
        selected_date = self.__view._dialog.date_selected

        return self.__model.make_order_report(selected_date)