import ttkbootstrap as ttk
from ttkbootstrap.constants import * # type: ignore
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
        self.__stock_menu.add_separator()
        self.__stock_menu.add_command(label="Relatório", accelerator="Ctrl+Shift+I", command=self.__controller.make_stock_report)
        self.bind_all("<Control-Shift-i>", lambda e: self.__controller.make_stock_report())
        self.__menu_bar.add_cascade(label="Estoque", menu=self.__stock_menu)

        # adiciona um menu de venda
        self.__sales_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__sales_menu.add_command(label="Vender", accelerator="Ctrl+V", command=self.__controller.open_order_window)
        self.bind_all("<Control-v>", lambda e: self.__controller.open_order_window())
        self.__sales_menu.add_separator()
        self.__sales_menu.add_command(label="Relatório", accelerator="Ctrl+Shift+V", command=self.__controller.make_sales_report)
        self.bind_all("<Control-Shift-v>", lambda e: self.__controller.make_sales_report())
        self.__menu_bar.add_cascade(label="Caixa", menu=self.__sales_menu)

        # adiciona um menu de ajuda
        self.__help_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__help_menu.add_command(label="Sobre", command=self.__controller.open_about_window)
        self.__menu_bar.add_cascade(label="Ajuda", menu=self.__help_menu)

        # adiciona um menu de créditos
        self.__credits_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__credits_menu.add_command(label="Créditos", command=self.__controller.open_credits_window)
        self.__menu_bar.add_cascade(label="Créditos", menu=self.__credits_menu)

        # adiciona um rodapé
        self.__footer = ttk.Label(self, text="$hopkeeper 2025 © Rafael Renó Corrêa - Todos os direitos reservados.", font=("Arial", 10), anchor="center")
        self.__footer.pack(side=BOTTOM, fill=X, pady=5)

    # rotina de encerramento gracioso
    def shutdown(self):
        if not self.__on_shutdown:
            self.__on_shutdown = True
            
            if msgbox.yesno("Deseja encerrar a aplicação?", "Sair do $hopkeeper") == "Sim":
                self.__controller.shutdown()
            else:
                self.__on_shutdown = False