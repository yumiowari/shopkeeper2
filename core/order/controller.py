from core.order.model import Model
from core.order.view import View
from core.order.model import ProductModel
from core.order.view import ProductView
from core.order.model import ConferOrderModel
from core.order.view import ConferOrderView

class Controller:
    def __init__(self, master=None, parent=None):
        self.__model = Model()
        self._view = View(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

        self._product_ctrl = None

    def on_close(self):
        if self._product_ctrl:
            self._product_ctrl.on_close()

        self.__model.on_close()

        self._view.destroy()

    def fetch_selected_items(self):
        return self.__model.fetch_selected_items()
    
    def commit_sale(self):
        return self.__model.commit_sale()

    def add_product(self):
        if self._product_ctrl is None or not self._product_ctrl._view.winfo_exists():
            self._product_ctrl = ProductController(master=self._view, parent=self)
        else: # se já existe, traz para frente
            self._product_ctrl._view.lift()

    def remove_product(self):
        item_name = self._view._selected_items_combo.get().split(')', 1)[1].strip()

        return self.__model.remove_product(item_name)

class ProductController:
    def __init__(self, master=None, parent=None):
        self.__model = ProductModel()
        self._view = ProductView(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def on_close(self):
        self.__model.on_close()

        self._view.destroy()

    def fetch_item_names(self):
        return self.__model.fetch_item_names()
    
    def confirm_product(self):
        item_name = self._view._item_name_combo.get()
        item_qty = self._view._item_qty_spin.get()

        return self.__model.confirm_product(item_name, item_qty)
    
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