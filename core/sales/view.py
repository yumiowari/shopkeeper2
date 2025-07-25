import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox as msgbox
from ttkbootstrap.tooltip import ToolTip as tooltip

class View(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl

        self.title("Inventário")
        self.geometry("600x450")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # cria um frame para o conteúdo principal
        self._main_frame = ttk.Frame(self)
        self._main_frame.pack(fill=BOTH, expand=True)

        # adiciona um rótulo ao frame principal
        self.__main_label = ttk.Label(self._main_frame, text="Registrar venda...", font=("Arial", 12))
        self.__main_label.pack(pady=20)

        # cria um frame superior
        self._top_frame = ttk.Frame(self._main_frame)
        self._top_frame.pack(side=TOP, padx=10, pady=10)

        # cria um frame inferior (para os botões)
        self.__bottom_frame = ttk.Frame(self._main_frame)
        self.__bottom_frame.pack(side=BOTTOM, padx=10, pady=10)

        self.__left_bottom_frame = ttk.Frame(self.__bottom_frame)
        self.__left_bottom_frame.pack(side=LEFT, padx=5, pady=5)

        self.__right_bottom_frame = ttk.Frame(self.__bottom_frame)
        self.__right_bottom_frame.pack(side=RIGHT, padx=5, pady=5)

        # cria um combobox para listar os itens selecionados
        self._selected_items_combo = ttk.Combobox(self._top_frame, state="readonly")
        self._selected_items_combo.config(values=self.__controller.fetch_selected_items())
        self._selected_items_combo_label = ttk.Label(self._top_frame, text="São os itens na comanda:")

        tooltip(self._selected_items_combo, "Lista dos itens selecionados na comanda.")

        self._selected_items_combo_label.pack(padx=5, pady=5)
        self._selected_items_combo.pack(padx=5, pady=5)

        # cria botões para registrar a venda
        self._commit_sale_btn = ttk.Button(self.__left_bottom_frame, text="Confirmar", command=self.__controller.commit_sale, bootstyle="success")
        self._cancel_sale_btn = ttk.Button(self.__left_bottom_frame, text="Cancelar", command=self.__controller.cancel_sale, bootstyle="danger")
        self._add_product_btn = ttk.Button(self.__right_bottom_frame, text="Adicionar produto", command=self.__controller.add_product)
        self._remove_product_btn = ttk.Button(self.__right_bottom_frame, text="Remover produto", command=self.__controller.remove_product, bootstyle="warning")

        tooltip(self._commit_sale_btn, "Registrar a comanda no banco de dados.")
        tooltip(self._cancel_sale_btn, "Cancelar a comanda.")
        tooltip(self._add_product_btn, "Adicionar um produto à comanda.")
        tooltip(self._remove_product_btn, "Remover um produto da comanda.")

        self._commit_sale_btn.pack(side=TOP, padx=5, pady=5)
        self._cancel_sale_btn.pack(side=TOP, padx=5, pady=5)
        self._add_product_btn.pack(side=BOTTOM, padx=5, pady=5)
        self._remove_product_btn.pack(side=BOTTOM, padx=5, pady=5)

    def on_close(self):
        self.__parent_ctrl.sales_ctrl = None
        self.destroy()