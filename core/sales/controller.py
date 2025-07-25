from core.sales.model import Model
from core.sales.view import View

class Controller:
    def __init__(self, master=None, parent=None):
        self.__model = Model()
        self._view = View(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def fetch_selected_items(self):
        return self.__model.fetch_selected_items()
    
    def fetch_item_names(self):
        return self.__model.fetch_item_names()
    
    def commit_sale(self):
        pass

    def cancel_sale(self):
        pass

    def add_product(self):
        pass

    def remove_product(self):
        pass