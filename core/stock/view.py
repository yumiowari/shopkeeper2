import ttkbootstrap as ttk
from ttkbootstrap.constants import * # type: ignore
from ttkbootstrap.dialogs import Messagebox as msgbox
from ttkbootstrap.tooltip import ToolTip as tooltip
import re

def validate_number(x) -> bool:
    """Valida se o input é número inteiro até 999"""
    if x == "":
        return True
    return x.isdigit() and int(x) <= 999

def validate_entry_number(x) -> bool:
    """Valida se o input é número inteiro entre -99 e 99, diferente de zero"""
    if x == "":
        return True
    try:
        n = int(x)

        if n >= -99 and n <= 99 and n != 0:
            return True
        else:
            return False
    except ValueError:
        return False
    
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
        self._notebook = ttk.Notebook(self)

        # CREATE
        self._create_frame = ttk.Frame(self._notebook)

        self._create_label = ttk.Label(self._create_frame, text="Cadastrar novo item no inventário...", font=("Arial", 12))
        
        self._create_item_name_entry = ttk.Entry(self._create_frame, width=20, validate="focus", validatecommand=(alpha_validator, '%P'))
        self._create_item_name_label = ttk.Label(self._create_frame, text="Nome do item:", font=("Arial", 10, "bold"))
        self._create_item_cost_entry = ttk.Entry(self._create_frame, width=10, validate="focus", validatecommand=(money_validator, '%P'))
        self._create_item_cost_label = ttk.Label(self._create_frame, text="Custo do item:", font=("Arial", 10, "bold"))
        self._create_item_price_entry = ttk.Entry(self._create_frame, width=10, validate="focus", validatecommand=(money_validator, '%P'))
        self._create_item_price_label = ttk.Label(self._create_frame, text="Preço de venda:", font=("Arial", 10, "bold"))
        self._create_item_qty_spin = ttk.Spinbox(self._create_frame, from_=0, to=999, width=5, validate="focus", validatecommand=(number_validator, '%P'))
        self._create_item_qty_label = ttk.Label(self._create_frame, text="Quantidade inicial:", font=("Arial", 10))

        self._create_confirm_btn = ttk.Button(self._create_frame, text="Cadastrar", command=self.create_item, bootstyle="success", width=10) # type: ignore

        self._create_label.pack(pady=10)
        self._create_item_name_label.pack(pady=5)
        self._create_item_name_entry.pack(pady=5)
        self._create_item_cost_label.pack(pady=5)
        self._create_item_cost_entry.pack(pady=5)
        self._create_item_price_label.pack(pady=5)
        self._create_item_price_entry.pack(pady=5)
        self._create_item_qty_label.pack(pady=5)
        self._create_item_qty_spin.pack(pady=5)

        self._create_confirm_btn.pack(pady=10)

        tooltip(self._create_item_name_entry, "Qual o nome do item?")
        tooltip(self._create_item_cost_entry, "Qual o custo de produção do item?")
        tooltip(self._create_item_price_entry, "Qual o preço de venda do item?")
        tooltip(self._create_item_qty_spin, "Qual a quantidade inicial do item?")
        tooltip(self._create_confirm_btn, "Confirma o cadastro do produto no inventário.")

        # READ (CONFER)
        self._confer_frame = ttk.Frame(self._notebook)

        self._confer_item_label = ttk.Label(self._confer_frame, text="Consultar item no inventário...", font=("Arial", 12))

        self._confer_item_name_combo = ttk.Combobox(self._confer_frame, width=20, validate="focus", validatecommand=(alpha_validator, '%P'))
        self._confer_item_name_combo.config(values=self.__controller.fetch_item_names())
        self._confer_item_name_combo_label = ttk.Label(self._confer_frame, text="Selecione o item:", font=("Arial", 10, "bold"))
        
        self._confer_confirm_btn = ttk.Button(self._confer_frame, text="Consultar", command=self.confer_item, bootstyle="info", width=10) # type: ignore

        self._confer_item_label.pack(pady=10)
        self._confer_item_name_combo_label.pack(pady=5)
        self._confer_item_name_combo.pack(pady=5)

        self._confer_confirm_btn.pack(pady=10)

        tooltip(self._confer_item_name_combo, "Qual o nome do item?")
        tooltip(self._confer_confirm_btn, "Confirma a consulta do produto no inventário.")

        # UPDATE
        self._update_frame = ttk.Frame(self._notebook)

        self._update_label = ttk.Label(self._update_frame, text="Atualizar item no inventário...", font=("Arial", 12))

        self._update_item_name_combo = ttk.Combobox(self._update_frame, width=20, validate="focus", validatecommand=(alpha_validator, '%P'))
        self._update_item_name_combo.config(values=self.__controller.fetch_item_names())
        self._update_item_name_combo_label = ttk.Label(self._update_frame, text="Selecione o item:", font=("Arial", 10, "bold"))
        self._update_item_cost_entry = ttk.Entry(self._update_frame, width=10, validate="focus", validatecommand=(money_validator, '%P'))
        self._update_item_cost_label = ttk.Label(self._update_frame, text="Novo custo do item:", font=("Arial", 10))
        self._update_item_price_entry = ttk.Entry(self._update_frame, width=10, validate="focus", validatecommand=(money_validator, '%P'))
        self._update_item_price_label = ttk.Label(self._update_frame, text="Novo preço de venda:", font=("Arial", 10))
        self._update_item_qty_spin = ttk.Spinbox(self._update_frame, from_=0, to=999, width=5, validate="focus", validatecommand=(number_validator, '%P'))
        self._update_item_qty_label = ttk.Label(self._update_frame, text="Nova quantidade:", font=("Arial", 10))

        self._update_confirm_btn = ttk.Button(self._update_frame, text="Atualizar", command=self.update_item, bootstyle="warning", width=10) # type: ignore

        self._update_label.pack(pady=10)
        self._update_item_name_combo_label.pack(pady=5)
        self._update_item_name_combo.pack(pady=5)
        self._update_item_cost_label.pack(pady=5)
        self._update_item_cost_entry.pack(pady=5)
        self._update_item_price_label.pack(pady=5)
        self._update_item_price_entry.pack(pady=5)
        self._update_item_qty_label.pack(pady=5)
        self._update_item_qty_spin.pack(pady=5)

        self._update_confirm_btn.pack(pady=10)

        tooltip(self._update_item_name_combo, "Qual o nome do item?")
        tooltip(self._update_item_cost_entry, "Qual o novo custo de produção do item?")
        tooltip(self._update_item_price_entry, "Qual o novo preço de venda do item?")
        tooltip(self._update_item_qty_spin, "Qual a nova quantidade do item?")
        tooltip(self._update_confirm_btn, "Confirma a atualização do produto no inventário.")

        # DELETE
        self._delete_frame = ttk.Frame(self._notebook)

        self._delete_item_label = ttk.Label(self._delete_frame, text="Remover item do inventário...", font=("Arial", 12))

        self._delete_item_name_combo = ttk.Combobox(self._delete_frame, width=20, validate="focus", validatecommand=(alpha_validator, '%P'))
        self._delete_item_name_combo.config(values=self.__controller.fetch_item_names())
        self._delete_item_name_combo_label = ttk.Label(self._delete_frame, text="Selecione o item:", font=("Arial", 10, "bold"))

        self._delete_confirm_btn = ttk.Button(self._delete_frame, text="Remover", command=self.delete_item, bootstyle="danger", width=10) # type: ignore

        self._delete_item_label.pack(pady=10)
        self._delete_item_name_combo_label.pack(pady=5)
        self._delete_item_name_combo.pack(pady=5)

        self._delete_confirm_btn.pack(pady=10)

        tooltip(self._delete_item_name_combo, "Qual o nome do item?")
        tooltip(self._delete_confirm_btn, "Confirma a remoção do produto do inventário.")

        self._notebook.add(self._create_frame, text="Cadastrar")
        self._notebook.add(self._confer_frame, text="Consultar")
        self._notebook.add(self._update_frame, text="Atualizar")
        self._notebook.add(self._delete_frame, text="Remover")

        self._notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def on_close(self):
        self.__parent_ctrl.stock_ctrl = None
        self.destroy()

    def create_item(self):
        item_name = self._create_item_name_entry.get()
        item_cost = self._create_item_cost_entry.get()
        item_price = self._create_item_price_entry.get()
        item_qty = self._create_item_qty_spin.get()
        
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

        if flag:
            res = self.__controller.create_item()

            if res == 0:
                msgbox.show_info(f"O produto \"{item_name}\" foi cadastrado no banco de dados.", "Sucesso")
            elif res == 1:
                msgbox.show_error(f"O produto \"{item_name}\" já existe no banco de dados.")
        
                flag = False
        if not flag:
            msgbox.show_error("O cadastro do produto falhou.", "Erro")

        self._create_item_name_entry.delete(0, 'end')
        self._create_item_cost_entry.delete(0, 'end')
        self._create_item_price_entry.delete(0, 'end')
        self._create_item_qty_spin.set("")

    def confer_item(self):
        item_name = self._confer_item_name_combo.get()

        flag = True

        # valida o campo de entrada
        if not item_name:
            msgbox.show_error("Um produto precisa ser selecionado", "Erro")

            flag = False

        if flag and not validate_alpha(item_name):
            msgbox.show_error("O nome do item deve conter apenas letras e ter no máximo 30 caracteres.", "Erro")

            flag = False

        if flag:
            item = self.__controller.confer_item()

            if item:
                output = "É o produto:\n\n"
                output += f"Nome: {item['name']}\n"
                output += f"Custo: R$ {item['cost']}\n"
                output += f"Preço: R$ {item['price']}\n"
                output += f"Quantidade: {item['qty']}\n"

                msgbox.show_info(output, "Sucesso")
            else:
                msgbox.show_error(f"O produto \"{item_name}\" não foi encontrado.")
        if not flag:
            msgbox.show_error("A consulta do produto falhou.", "Erro")
        
        self._confer_item_name_combo.set("")

    def update_item(self):
        item_name = self._update_item_name_combo.get()
        item_cost = self._update_item_cost_entry.get()
        item_price = self._update_item_price_entry.get()
        item_qty = self._update_item_qty_spin.get()
        
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

        if flag:        
            res = self.__controller.update_item()

            if res == 0:
                msgbox.show_info(f"O produto \"{item_name}\" foi atualizado no banco de dados.", "Sucesso")
            elif res == 1:
                msgbox.show_warning("Nenhum atributo do produto foi alterado.", "Aviso")
            elif res == 2:
                msgbox.show_error(f"O produto \"{item_name}\" não foi encontrado.")
        if not flag:
            msgbox.show_error("O cadastro do produto falhou.", "Erro")

        self._update_item_name_combo.set("")
        self._update_item_cost_entry.delete(0, 'end')
        self._update_item_price_entry.delete(0, 'end')
        self._update_item_qty_spin.set("")

    def delete_item(self):
        item_name = self._delete_item_name_combo.get()

        flag = True

        # valida o campo de entrada
        if not item_name:
            msgbox.show_error("Um produto precisa ser selecionado", "Erro")

            flag = False

        if flag and not validate_alpha(item_name):
            msgbox.show_error("O nome do item deve conter apenas letras e ter no máximo 30 caracteres.", "Erro")

            flag = False

        if flag:
            res = self.__controller.delete_item()

            if res == 0:
                msgbox.show_info(f"O produto \"{item_name}\" foi removido do banco de dados.", "Sucesso")
            elif res == 1:
                msgbox.show_error
        if not flag:
            msgbox.show_error("A remoção do produto falhou.", "Erro")

        self._delete_item_name_combo.set("")

class EntryView(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl

        self.title("Entrada")
        self.geometry("400x300")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # observers
        alpha_validator = self.register(validate_alpha)
        number_validator = self.register(validate_entry_number)

        self._entry_frame = ttk.Frame(self)

        self._entry_label = ttk.Label(self._entry_frame, text="Registrar entrada/saída de produtos...", font=("Arial", 12))

        self._entry_item_name_combo = ttk.Combobox(self._entry_frame, width=20, validate="focus", validatecommand=(alpha_validator, '%P'))
        self._entry_item_name_combo.config(values=self.__controller.fetch_item_names())
        self._entry_item_name_combo_label = ttk.Label(self._entry_frame, text="Selecione o item:", font=("Arial", 10, "bold"))
        self._entry_item_qty_spin = ttk.Spinbox(self._entry_frame, from_=-99, to=99, width=5, validate="focus", validatecommand=(number_validator, '%P'))
        self._entry_item_qty_label = ttk.Label(self._entry_frame, text="Nova quantidade:", font=("Arial", 10))

        self._entry_confirm_btn = ttk.Button(self._entry_frame, text="Registrar", command=self.entry_item, bootstyle="primary", width=10) # type: ignore

        self._entry_label.pack(pady=10)
        self._entry_item_name_combo_label.pack(pady=5)
        self._entry_item_name_combo.pack(pady=5)
        self._entry_item_qty_label.pack(pady=5)
        self._entry_item_qty_spin.pack(pady=5)

        self._entry_confirm_btn.pack(pady=10)

        self._entry_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tooltip(self._entry_item_name_combo, "Qual o nome do item?")
        tooltip(self._entry_item_qty_spin, "Qual a quantidade a ser incrementada?")
        tooltip(self._entry_confirm_btn, "Confirma o registro da entrada/saída do produto no inventário.")

    def on_close(self):
        self.__parent_ctrl.stock_entry_ctrl = None
        self.destroy()

    def entry_item(self):
        item_name = self._entry_item_name_combo.get()
        item_qty = self._entry_item_qty_spin.get()
        
        flag = True

        # valida os campos de entrada
        if not item_name:
            msgbox.show_error("Um produto precisa ser selecionado.", "Erro")
            
            flag = False

        if flag and not validate_alpha(item_name):
            msgbox.show_error("O nome do item deve conter apenas letras e ter no máximo 30 caracteres.", "Erro")
            
            flag = False
        if flag and item_qty and not validate_entry_number(item_qty):
            msgbox.show_error("A quantidade deve ser um número inteiro entre -99 e 99, diferente de zero.", "Erro")

            flag = False

        if flag:        
            res = self.__controller.entry_item()

            if res == 0:
                msgbox.show_info(f"A quantidade do produto \"{item_name}\" foi alterada no banco de dados.", "Sucesso")
            elif res == 1:
                msgbox.show_error(f"O produto \"{item_name}\" não foi encontrado.")
        if not flag:
            msgbox.show_error("O registro da entrada do produto falhou.", "Erro")

        self._entry_item_name_combo.set("")
        self._entry_item_qty_spin.set("")