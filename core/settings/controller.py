from core.settings.model import Model
from core.settings.view import View
from ttkbootstrap import Style

class Controller:
    def __init__(self, master=None, parent=None):
        self.__model = Model()
        self._view = View(self, parent_ctrl=parent)
        self._view.transient(master)
        self._view.grab_set()

    def confirm_theme(self):
        theme_name = self._view._theme_name_combo.get()

        Style().theme_use(theme_name)

        