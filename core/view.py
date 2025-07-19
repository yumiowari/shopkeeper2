import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class View(ttk.Window):
    def __init__(self, controller):
        super().__init__(themename="litera")
        self.controller = controller
        self.title("Shopkeeper")
        self.geometry("800x600")

        # cria um frame para o conteúdo principal
        self.__main_frame = ttk.Frame(self)
        self.__main_frame.pack(fill=BOTH, expand=True)

        # adiciona um rótulo ao frame principal
        self.__main_label = ttk.Label(self.__main_frame, text="Seja bem-vindo ao Shopkeeper!", font=("Arial", 16))
        self.__main_label.pack(pady=20)

        # cria um barra de menu
        self.__menu_bar = ttk.Menu(self)
        self.config(menu=self.__menu_bar)

        # adiciona um menu de arquivo
        self.__file_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__file_menu.add_command(label="Sair", command=self.quit)
        self.__menu_bar.add_cascade(label="Arquivo", menu=self.__file_menu)

        # adiciona um menu de estoque
        self.__stock_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__stock_menu.add_command(label="Inventário", command=self.controller.open_stock_window)
        self.__menu_bar.add_cascade(label="Estoque", menu=self.__stock_menu)