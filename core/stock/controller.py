from core.stock.model import Model
from core.stock.view import View

class Controller:
    def __init__(self, master=None, parent=None):
        self.model = Model()
        self.view = View(self, parent_ctrl=parent)
        self.view.transient(master)
        self.view.grab_set()