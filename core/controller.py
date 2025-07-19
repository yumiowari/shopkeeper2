from core.model import Model
from core.view import View
from core.toplevel.controller import TopController

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def run(self):
        self.view.mainloop()

    def handle_action(self):
        # Handle the action triggered by the button in the view
        print("Button clicked! Action handled.")

    def on_open_new_window(self):
        TopController(master=self.view)