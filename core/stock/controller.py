from core.stock.model import CRUDModel
from core.stock.view import CRUDView
from core.stock.model import EntryModel
from core.stock.view import EntryView

class CRUDController:
    def __init__(self, master=None, parent=None):
        self.__model = CRUDModel()
        self._view = CRUDView(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def fetch_product_names(self):
        return self.__model.fetch_product_names()
    
    def fetch_product_categories(self):
        return self.__model.fetch_product_categories()

    def create_product(self):
        product_name = self._view._create_product_name_entry.get()
        product_category = self._view._create_product_category_combo.get()
        product_cost = self._view._create_product_cost_entry.get().replace(',', '.')
        product_price = self._view._create_product_price_entry.get().replace(',', '.')
        product_qty = self._view._create_product_qty_spin.get()

        return self.__model.create_product(product_name, product_category, product_cost, product_price, product_qty)

    def confer_product(self):
        product_name = self._view._confer_product_name_combo.get()

        return self.__model.confer_product(product_name)

    def update_product(self):
        product_name = self._view._update_product_name_combo.get()
        product_category = self._view._update_product_category_combo.get()
        product_cost = self._view._update_product_cost_entry.get().replace(',', '.')
        product_price = self._view._update_product_price_entry.get().replace(',', '.')
        product_qty = self._view._update_product_qty_spin.get()

        return self.__model.update_product(product_name, product_category, product_cost, product_price, product_qty)

    def delete_product(self):
        product_name = self._view._delete_product_name_combo.get()

        return self.__model.delete_product(product_name)
    
class EntryController:
    def __init__(self, master=None, parent=None):
        self.__model = EntryModel()
        self._view = EntryView(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def fetch_product_names(self):
        return self.__model.fetch_product_names()
    
    def entry_product(self):
        product_name = self._view._entry_product_name_combo.get()
        entry_qty = self._view._entry_product_qty_spin.get()

        return self.__model.entry_product(product_name, entry_qty)