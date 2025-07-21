import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox as msgbox
import re

def validate_number(x) -> bool:
    """Valida se o input é número inteiro até 999"""
    if x == "":
        return True
    return x.isdigit() and int(x) <= 999
    
def validate_alpha(x) -> bool:
    """Valida se o input é alfabético e até 30 caracteres"""
    return (x == "" or not x.isdigit()) and len(x) <= 30
    
def validate_money(x) -> bool:
    """Valida se o input é um valor monetário até 99,99"""
    if x == "":
        return True
    if not re.fullmatch(r"\d{1,2}([.,]\d{0,2})?", x):
        return False
    try:
        val = float(x.replace(",", "."))

        return val <= 99.99
    except ValueError:
        return False

class View(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl

        self.title("Inventário")
        self.geometry("600x450")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # observers
        alpha_validator = self.register(validate_alpha)
        number_validator = self.register(validate_number)
        money_validator = self.register(validate_money)

        ### CRUDs
        self.__notebook = ttk.Notebook(self)

        # CREATE
        self.__create_frame = ttk.Frame(self.__notebook)

        self.__create_label = ttk.Label(self.__create_frame, text="Cadastrar novo item no inventário...", font=("Arial", 12))
        
        self.__create_item_name_entry = ttk.Entry(self.__create_frame, width=20, validate="focus", validatecommand=(alpha_validator, '%P'))
        self.__create_item_name_label = ttk.Label(self.__create_frame, text="Nome do item:", font=("Arial", 10, "bold"))
        self.__create_item_cost_entry = ttk.Entry(self.__create_frame, width=10, validate="focus", validatecommand=(money_validator, '%P'))
        self.__create_item_cost_label = ttk.Label(self.__create_frame, text="Custo do item:", font=("Arial", 10, "bold"))
        self.__create_item_price_entry = ttk.Entry(self.__create_frame, width=10, validate="focus", validatecommand=(money_validator, '%P'))
        self.__create_item_price_label = ttk.Label(self.__create_frame, text="Preço de venda:", font=("Arial", 10, "bold"))
        self.__create_item_qty_spin = ttk.Spinbox(self.__create_frame, from_=0, to=999, width=10, validate="focus", validatecommand=(number_validator, '%P'))
        self.__create_item_qty_label = ttk.Label(self.__create_frame, text="Quantidade inicial:", font=("Arial", 10))

        self.__create_confirm_btn = ttk.Button(self.__create_frame, text="Cadastrar", command=self.create_item)

        self.__create_label.pack(pady=10)
        self.__create_item_name_label.pack(pady=5)
        self.__create_item_name_entry.pack(pady=5)
        self.__create_item_cost_label.pack(pady=5)
        self.__create_item_cost_entry.pack(pady=5)
        self.__create_item_price_label.pack(pady=5)
        self.__create_item_price_entry.pack(pady=5)
        self.__create_item_qty_label.pack(pady=5)
        self.__create_item_qty_spin.pack(pady=5)

        self.__create_confirm_btn.pack(pady=10)

        # READ (CONFER)
        self.__confer_frame = ttk.Frame(self.__notebook)

        self.__confer_item_label = ttk.Label(self.__confer_frame, text="Consultar item no inventário...", font=("Arial", 12))

        self.__confer_item_name_combo = ttk.Combobox(self.__confer_frame, width=20, validate="focus", validatecommand=(alpha_validator, '%P'))
        self.__confer_item_name_combo_label = ttk.Label(self.__confer_frame, text="Selecione o item:", font=("Arial", 10, "bold"))
        
        self.__confer_confirm_btn = ttk.Button(self.__confer_frame, text="Consultar", command=self.confer_item)

        self.__confer_item_label.pack(pady=10)
        self.__confer_item_name_combo_label.pack(pady=5)
        self.__confer_item_name_combo.pack(pady=5)

        self.__confer_confirm_btn.pack(pady=10)

        # UPDATE
        self.__update_frame = ttk.Frame(self.__notebook)

        self.__update_label = ttk.Label(self.__update_frame, text="Atualizar item no inventário...", font=("Arial", 12))

        self.__update_item_name_combo = ttk.Combobox(self.__update_frame, width=20, validate="focus", validatecommand=(alpha_validator, '%P'))
        self.__update_item_name_combo_label = ttk.Label(self.__update_frame, text="Selecione o item:", font=("Arial", 10, "bold"))
        self.__update_item_cost_entry = ttk.Entry(self.__update_frame, width=10, validate="focus", validatecommand=(money_validator, '%P'))
        self.__update_item_cost_label = ttk.Label(self.__update_frame, text="Novo custo do item:", font=("Arial", 10))
        self.__update_item_price_entry = ttk.Entry(self.__update_frame, width=10, validate="focus", validatecommand=(money_validator, '%P'))
        self.__update_item_price_label = ttk.Label(self.__update_frame, text="Novo preço de venda:", font=("Arial", 10))
        self.__update_item_qty_spin = ttk.Spinbox(self.__update_frame, from_=0, to=999, width=10, validate="focus", validatecommand=(number_validator, '%P'))
        self.__update_item_qty_label = ttk.Label(self.__update_frame, text="Nova quantidade:", font=("Arial", 10))

        self.__update_confirm_btn = ttk.Button(self.__update_frame, text="Atualizar", command=self.update_item)

        self.__update_label.pack(pady=10)
        self.__update_item_name_combo_label.pack(pady=5)
        self.__update_item_name_combo.pack(pady=5)
        self.__update_item_cost_label.pack(pady=5)
        self.__update_item_cost_entry.pack(pady=5)
        self.__update_item_price_label.pack(pady=5)
        self.__update_item_price_entry.pack(pady=5)
        self.__update_item_qty_label.pack(pady=5)
        self.__update_item_qty_spin.pack(pady=5)

        self.__update_confirm_btn.pack(pady=10)

        # DELETE
        self.__delete_frame = ttk.Frame(self.__notebook)

        self.__delete_item_label = ttk.Label(self.__delete_frame, text="Remover item do inventário...", font=("Arial", 12))

        self.__delete_item_name_combo = ttk.Combobox(self.__delete_frame, width=20, validate="focus", validatecommand=(alpha_validator, '%P'))
        self.__delete_item_name_combo_label = ttk.Label(self.__delete_frame, text="Selecione o item:", font=("Arial", 10, "bold"))

        self.__delete_confirm_btn = ttk.Button(self.__delete_frame, text="Remover", command=self.delete_item)

        self.__delete_item_label.pack(pady=10)
        self.__delete_item_name_combo_label.pack(pady=5)
        self.__delete_item_name_combo.pack(pady=5)

        self.__delete_confirm_btn.pack(pady=10)

        self.__notebook.add(self.__create_frame, text="Cadastrar")
        self.__notebook.add(self.__confer_frame, text="Consultar")
        self.__notebook.add(self.__update_frame, text="Atualizar")
        self.__notebook.add(self.__delete_frame, text="Remover")

        self.__notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def on_close(self):
        self.__parent_ctrl.stock_ctrl = None
        self.destroy()

    def create_item(self):
        item_name = self.__create_item_name_entry.get()
        item_cost = self.__create_item_cost_entry.get()
        item_price = self.__create_item_price_entry.get()
        item_qty = self.__create_item_qty_spin.get()
        
        flag = True

        # valida os campos de entrada
        if not item_name or not item_cost or not item_price:
            msgbox.show_error("Todos os campos obrigatórios devem ser preenchidos.", "Erro")
            
            flag = False

        if flag and not validate_alpha(item_name):
            msgbox.show_error("O nome do item deve conter apenas letras e ter no máximo 30 caracteres.", "Erro")
            
            flag = False
        if flag and not validate_money(item_cost):
            msgbox.show_error("O custo do item deve ser um valor monetário válido menor que 99,99.", "Erro")

            flag = False
        if flag and not validate_money(item_price):
            msgbox.show_error("O preço de venda deve ser um valor monetário válido menor que 99,99.", "Erro")

            flag = False
        if flag and not validate_number(item_qty):
            msgbox.show_error("A quantidade deve ser um número inteiro entre 0 e 999.", "Erro")

            flag = False

        if flag and self.__controller.create_item():
            msgbox.show_info(f"O produto \"{item_name}\" foi cadastrado no banco de dados.", "Sucesso")
        else:
            msgbox.show_error("O cadastro do produto falhou.", "Erro")

        self.__create_item_name_entry.delete(0, 'end')
        self.__create_item_cost_entry.delete(0, 'end')
        self.__create_item_price_entry.delete(0, 'end')
        self.__create_item_qty_spin.set("")

    def confer_item(self):
        item_name = self.__confer_item_name_combo.get()

        flag = True

        # valida o campo de entrada
        if not item_name:
            msgbox.show_error("Um produto precisa ser selecionado", "Erro")

            flag = False

        if flag and not validate_alpha(item_name):
            msgbox.show_error("O nome do item deve conter apenas letras e ter no máximo 30 caracteres.", "Erro")

            flag = False

        if flag and self.__controller.confer_item():
            msgbox.show_info("É o produto: (...)", "Sucesso")
        else:
            msgbox.show_error("A consulta do produto falhou.", "Erro")
        
        self.__confer_item_name_combo.set("")

    def update_item(self):
        item_name = self.__update_item_name_combo.get()
        item_cost = self.__update_item_cost_entry.get()
        item_price = self.__update_item_price_entry.get()
        item_qty = self.__update_item_qty_spin.get()
        
        flag = True

        # valida os campos de entrada
        if not item_name:
            msgbox.show_error("Um produto precisa ser selecionado.", "Erro")
            
            flag = False

        if flag and not validate_alpha(item_name):
            msgbox.show_error("O nome do item deve conter apenas letras e ter no máximo 30 caracteres.", "Erro")
            
            flag = False
        if flag and item_cost and not validate_money(item_cost):
            msgbox.show_error("O custo do item deve ser um valor monetário válido menor que 99,99.", "Erro")

            flag = False
        if flag and item_price and not validate_money(item_price):
            msgbox.show_error("O preço de venda deve ser um valor monetário válido menor que 99,99.", "Erro")

            flag = False
        if flag and item_qty and not validate_number(item_qty):
            msgbox.show_error("A quantidade deve ser um número inteiro entre 0 e 999.", "Erro")

            flag = False

        if flag and not item_cost and not item_price and not item_qty:
            msgbox.show_warning("Nenhum atributo do produto foi alterado.", "Aviso")
        elif flag and self.__controller.create_item():
            msgbox.show_info(f"O produto \"{item_name}\" foi atualizado no banco de dados.", "Sucesso")
        else:
            msgbox.show_error("O cadastro do produto falhou.", "Erro")

        self.__update_item_name_combo.set("")
        self.__update_item_cost_entry.delete(0, 'end')
        self.__update_item_price_entry.delete(0, 'end')
        self.__update_item_qty_spin.set("")

    def delete_item(self):
        item_name = self.__delete_item_name_combo.get()

        flag = True

        # valida o campo de entrada
        if not item_name:
            msgbox.show_error("Um produto precisa ser selecionado", "Erro")

            flag = False

        if flag and not validate_alpha(item_name):
            msgbox.show_error("O nome do item deve conter apenas letras e ter no máximo 30 caracteres.", "Erro")

            flag = False

        if flag and self.__controller.delete_item():
            msgbox.show_info(f"O produto \"{item_name}\" foi removido do banco de dados.", "Sucesso")
        else:
            msgbox.show_error("A remoção do produto falhou.", "Erro")

        self.__delete_item_name_combo.set("")