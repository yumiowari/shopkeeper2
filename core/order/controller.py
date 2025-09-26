from core.order.model import CreateOrderModel
from core.order.view import CreateOrderView
from core.order.model import SelectProductModel
from core.order.view import SelectProductView
from core.order.model import ConferOrderModel
from core.order.view import ConferOrderView

class CreateOrderController:
    def __init__(self, master=None, parent=None):
        self.__model = CreateOrderModel()
        self._view = CreateOrderView(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

        self._select_product_ctrl = None

    def on_close(self):
        if self._select_product_ctrl:
            self._select_product_ctrl.on_close()

        self.__model.on_close()

        self._view.destroy()

    def fetch_selected_products(self):
        return self.__model.fetch_selected_products()
    
    def commit_sale(self):
        return self.__model.commit_sale()

    def add_product(self):
        if self._select_product_ctrl is None or not self._select_product_ctrl._view.winfo_exists():
            self._select_product_ctrl = SelectProductController(master=self._view, parent=self)
        else: # se já existe, traz para frente
            self._select_product_ctrl._view.lift()

    def remove_product(self):
        product_name = self._view._selected_products_combo.get().split(')', 1)[1].strip()

        return self.__model.remove_product(product_name)

class SelectProductController:
    def __init__(self, master=None, parent=None):
        self.__model = SelectProductModel()
        self._view = SelectProductView(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def on_close(self):
        self.__model.on_close()

        self._view.destroy()

    def fetch_product_names(self):
        return self.__model.fetch_product_names()
    
    def confirm_product(self):
        product_name = self._view._product_name_combo.get()
        product_qty = self._view._product_qty_spin.get()

        return self.__model.confirm_product(product_name, product_qty)
    
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