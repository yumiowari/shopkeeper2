from core.settings.model import Model
from core.settings.view import View

class Controller:
    def __init__(self, master=None, parent=None):
        self.__model = Model()
        self._view = View(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()