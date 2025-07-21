import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox as msgbox

class View(ttk.Window):
    def __init__(self, controller):
        super().__init__(themename="litera")
        self.__controller = controller
        self.title("$hopkeeper")
        self.geometry("800x600")
        self.resizable(False, False)
        self.__on_shutdown = False

        # cria um frame para o conteúdo principal
        self.__main_frame = ttk.Frame(self)
        self.__main_frame.pack(fill=BOTH, expand=True)

        # adiciona um rótulo ao frame principal
        self.__main_label = ttk.Label(self.__main_frame, text="Seja bem-vindo ao $hopkeeper!", font=("Arial", 16))
        self.__main_label.pack(pady=20)

        # cria um barra de menu
        self.__menu_bar = ttk.Menu(self)
        self.config(menu=self.__menu_bar)

        # adiciona um menu de arquivo
        self.__file_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__file_menu.add_command(label="Preferências")
        self.__file_menu.add_separator()
        self.__file_menu.add_command(label="Sair", accelerator="Ctrl+Q", command=self.shutdown)
        self.bind_all("<Control-q>", lambda e: self.shutdown())
        self.__menu_bar.add_cascade(label="Arquivo", menu=self.__file_menu)

        # adiciona um menu de estoque
        self.__stock_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__stock_menu.add_command(label="Inventário", accelerator="Ctrl+I", command=self.__controller.open_stock_window)
        self.bind_all("<Control-i>", lambda e: self.__controller.open_stock_window())
        self.__stock_menu.add_command(label="Entrada", accelerator="Ctrl+E", command=self.__controller.open_stock_entry_window)
        self.bind_all("<Control-e>", lambda e: self.__controller.open_stock_entry_window())
        self.__menu_bar.add_cascade(label="Estoque", menu=self.__stock_menu)

    # rotina de encerramento gracioso
    def shutdown(self):
        if not self.__on_shutdown:
            self.__on_shutdown = True
            
            if msgbox.yesno("Deseja encerrar a aplicação?", "Sair do $hopkeeper") == "Sim":
                self.__controller.shutdown()
            else:
                self.__on_shutdown = False