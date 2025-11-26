from core.order.model import CreateOrderModel
from core.order.view import CreateOrderView
from core.order.model import ConferOrderModel
from core.order.view import ConferOrderView

class CreateOrderController:
    def __init__(self, master=None, parent=None):
        self.__model = CreateOrderModel()
        self._view = CreateOrderView(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def on_close(self):
        self.__model.on_close()

        self._view.destroy()
    
    def commit_order(self, order):
        return self.__model.commit_order(order)
    
    def fetch_product_map(self):
        return self.__model.fetch_product_map()

class ConferOrderController:
    def __init__(self, master=None, parent=None):
        self.__model = ConferOrderModel()
        self._view = ConferOrderView(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def on_close(self):
        self.__model.on_close()

        self._view.destroy()

    def fetch_order_list(self):
        selected_date = self._view._date_entry.get_date()

        return self.__model.fetch_order_list(selected_date)
    
    def fetch_order(self):
        selected_timestamp = self._view._timestamp_combo.get()

        return self.__model.fetch_order(selected_timestamp)
    
    def fetch_stock(self):
        return self.__model.fetch_stock()
    
    def undo_specific_order(self):
        selected_timestamp = self._view._timestamp_combo.get()

        return self.__model.undo_specific_order(selected_timestamp)