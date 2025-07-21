from core.stock.model import Model
from core.stock.view import View

class Controller:
    def __init__(self, master=None, parent=None):
        self.__model = Model()
        self.__view = View(self, parent_ctrl=parent)
        self.__view.transient(master)
        self.__view.grab_set()

    def create_item(self):
        pass