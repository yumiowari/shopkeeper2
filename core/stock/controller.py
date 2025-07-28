from core.stock.model import Model
from core.stock.view import View
from core.stock.model import EntryModel
from core.stock.view import EntryView

class Controller:
    def __init__(self, master=None, parent=None):
        self.__model = Model()
        self._view = View(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def fetch_item_names(self):
        return self.__model.fetch_item_names()

    def create_item(self):
        item_name = self._view._create_item_name_entry.get()
        item_cost = self._view._create_item_cost_entry.get().replace(',', '.')
        item_price = self._view._create_item_price_entry.get().replace(',', '.')
        item_qty = self._view._create_item_qty_spin.get()

        return self.__model.create_item(item_name, item_cost, item_price, item_qty)

    def confer_item(self):
        item_name = self._view._confer_item_name_combo.get()

        return self.__model.confer_item(item_name)

    def update_item(self):
        item_name = self._view._update_item_name_combo.get()
        item_cost = self._view._update_item_cost_entry.get().replace(',', '.')
        item_price = self._view._update_item_price_entry.get().replace(',', '.')
        item_qty = self._view._update_item_qty_spin.get()

        return self.__model.update_item(item_name, item_cost, item_price, item_qty)

    def delete_item(self):
        item_name = self._view._delete_item_name_combo.get()

        return self.__model.delete_item(item_name)
    
class EntryController:
    def __init__(self, master=None, parent=None):
        self.__model = EntryModel()
        self._view = EntryView(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def fetch_item_names(self):
        return self.__model.fetch_item_names()
    
    def entry_item(self):
        item_name = self._view._entry_item_name_combo.get()
        entry_qty = self._view._entry_item_qty_spin.get()

        return self.__model.entry_item(item_name, entry_qty)