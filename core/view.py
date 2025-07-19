import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class View(ttk.Window):
    def __init__(self, controller):
        super().__init__(themename="litera")
        self.controller = controller
        self.title("Shopkeeper")
        self.geometry("800x600")

        # Create a frame for the main content
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Add a label to the main frame
        self.label = ttk.Label(self.main_frame, text="Welcome to Shopkeeper!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Add a button to trigger an action
        self.action_button = ttk.Button(self.main_frame, text="Click Me", command=self.controller.handle_action)
        self.action_button.pack(pady=10)

        self.button_open = ttk.Button(
            self.main_frame,
            text="Abrir nova janela",
            command=self.controller.on_open_new_window
        )
        self.button_open.pack(pady=5)