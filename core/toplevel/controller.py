from core.toplevel.model import Model
from core.toplevel.view import View

class TopController:
    def __init__(self, master=None):
        self.model = Model()
        self.view = View(self)
        self.view.transient(master)
        self.view.grab_set()

    def get_message(self):
        return self.model.message
