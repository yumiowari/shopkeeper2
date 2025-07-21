from core.stock.model import Model
from core.stock.view import View

class Controller:
    def __init__(self, master=None, parent=None):
        self.__model = Model()
        self._view = View(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def create_item(self):
        return True

    def confer_item(self):
        pass

    def update_item(self):
        pass

    def delete_item(self):
        pass