import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class View(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl

        self.title("Inventário")
        self.geometry("600x450")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.__notebook = ttk.Notebook(self)

        # CREATE
        self.__create_frame = ttk.Frame(self.__notebook)

        self.__create_label = ttk.Label(self.__create_frame, text="Cadastrar novo item no inventário...", font=("Arial", 12))
        
        self.__create_item_name_entry = ttk.Entry(self.__create_frame, width=20)
        self.__create_item_name_label = ttk.Label(self.__create_frame, text="Nome do item:", font=("Arial", 10, "bold"))
        self.__create_item_cost_entry = ttk.Entry(self.__create_frame, width=10)
        self.__create_item_cost_label = ttk.Label(self.__create_frame, text="Custo do item:", font=("Arial", 10, "bold"))
        self.__create_item_price_entry = ttk.Entry(self.__create_frame, width=10)
        self.__create_item_price_label = ttk.Label(self.__create_frame, text="Preço de venda:", font=("Arial", 10, "bold"))
        self.__create_item_qty_entry = ttk.Entry(self.__create_frame, width=10)
        self.__create_item_qty_label = ttk.Label(self.__create_frame, text="Quantidade inicial:", font=("Arial", 10))

        self.__create_confirm_btn = ttk.Button(self.__create_frame, text="Cadastrar", command=self.__controller.create_item)

        self.__create_label.pack(pady=10)
        self.__create_item_name_label.pack(pady=5)
        self.__create_item_name_entry.pack(pady=5)
        self.__create_item_cost_label.pack(pady=5)
        self.__create_item_cost_entry.pack(pady=5)
        self.__create_item_price_label.pack(pady=5)
        self.__create_item_price_entry.pack(pady=5)
        self.__create_item_qty_label.pack(pady=5)
        self.__create_item_qty_entry.pack(pady=5)

        self.__create_confirm_btn.pack(pady=10)

        # READ (CONFER)
        self.__confer_frame = ttk.Frame(self.__notebook)

        self.__confer_item_label = ttk.Label(self.__confer_frame, text="Consultar item no inventário...", font=("Arial", 12))

        self.__confer_item_combo = ttk.Combobox(self.__confer_frame, width=20)
        self.__confer_item_combo_label = ttk.Label(self.__confer_frame, text="Selecione o item:", font=("Arial", 10, "bold"))
        
        self.__confer_confirm_btn = ttk.Button(self.__confer_frame, text="Consultar", command=self.__controller.confer_item)

        self.__confer_item_label.pack(pady=10)
        self.__confer_item_combo_label.pack(pady=5)
        self.__confer_item_combo.pack(pady=5)

        self.__confer_confirm_btn.pack(pady=10)

        # UPDATE
        self.__update_frame = ttk.Frame(self.__notebook)

        self.__update_label = ttk.Label(self.__update_frame, text="Atualizar item no inventário...", font=("Arial", 12))
        
        self.__update_item_combo = ttk.Combobox(self.__update_frame, width=20)
        self.__update_item_combo_label = ttk.Label(self.__update_frame, text="Selecione o item:", font=("Arial", 10, "bold"))
        self.__update_item_cost_entry = ttk.Entry(self.__update_frame, width=10)
        self.__update_item_cost_label = ttk.Label(self.__update_frame, text="Novo custo do item:", font=("Arial", 10))
        self.__update_item_price_entry = ttk.Entry(self.__update_frame, width=10)
        self.__update_item_price_label = ttk.Label(self.__update_frame, text="Novo preço de venda:", font=("Arial", 10))
        self.__update_item_qty_entry = ttk.Entry(self.__update_frame, width=10)
        self.__update_item_qty_label = ttk.Label(self.__update_frame, text="Nova quantidade:", font=("Arial", 10))

        self.__update_confirm_btn = ttk.Button(self.__update_frame, text="Atualizar", command=self.__controller.update_item)

        self.__update_label.pack(pady=10)
        self.__update_item_combo_label.pack(pady=5)
        self.__update_item_combo.pack(pady=5)
        self.__update_item_cost_label.pack(pady=5)
        self.__update_item_cost_entry.pack(pady=5)
        self.__update_item_price_label.pack(pady=5)
        self.__update_item_price_entry.pack(pady=5)
        self.__update_item_qty_label.pack(pady=5)
        self.__update_item_qty_entry.pack(pady=5)

        self.__update_confirm_btn.pack(pady=10)

        # DELETE
        self.__delete_frame = ttk.Frame(self.__notebook)

        self.__delete_item_label = ttk.Label(self.__delete_frame, text="Remover item do inventário...", font=("Arial", 12))

        self.__delete_item_combo = ttk.Combobox(self.__delete_frame, width=20)
        self.__delete_item_combo_label = ttk.Label(self.__delete_frame, text="Selecione o item:", font=("Arial", 10, "bold"))

        self.__delete_confirm_btn = ttk.Button(self.__delete_frame, text="Remover", command=self.__controller.delete_item)

        self.__delete_item_label.pack(pady=10)
        self.__delete_item_combo_label.pack(pady=5)
        self.__delete_item_combo.pack(pady=5)

        self.__delete_confirm_btn.pack(pady=10)

        self.__notebook.add(self.__create_frame, text="Cadastrar")
        self.__notebook.add(self.__confer_frame, text="Consultar")
        self.__notebook.add(self.__update_frame, text="Atualizar")
        self.__notebook.add(self.__delete_frame, text="Remover")

        self.__notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def on_close(self):
        self.__parent_ctrl.stock_ctrl = None
        self.destroy()