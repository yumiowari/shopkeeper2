import ttkbootstrap as ttk
from ttkbootstrap.constants import * # type: ignore
from ttkbootstrap.dialogs import Messagebox as msgbox
from ttkbootstrap.tooltip import ToolTip as tooltip

def validate_alpha(x) -> bool:
    '''Valida se o input é alfabético e até 30 caracteres'''
    return (x == '' or not x.isdigit()) and len(x) <= 30

def validate_number(x) -> bool:
    '''Valida se o input é número inteiro entre 1 e 999'''
    if x == '':
        return True
    return x.isdigit() and int(x) <= 999 and int(x) >= 1

class View(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl
        self.__on_close = False
        self.__on_item_removal = False

        self.title('Comanda')
        self.geometry('600x450')
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.bind_all('<Escape>', lambda e: self.on_escape())

        # cria um frame para o conteúdo principal
        self._main_frame = ttk.Frame(self)
        self._main_frame.pack(fill=BOTH, expand=True)
        # X - Preenche a largura
        # Y - Preenche a altura
        # BOTH - Preenche ambos
        # NONE - Não preenche nada

        # adiciona um rótulo ao frame principal
        self.__main_label = ttk.Label(self._main_frame, text='Cadastrar comanda...', font=('Arial', 12))
        self.__main_label.pack(pady=20)

        # cria um frame superior
        self._top_frame = ttk.Frame(self._main_frame)
        self._top_frame.pack(fill=NONE, side=TOP, padx=10, pady=10)

        # cria um frame inferior (para os botões)
        self.__bottom_frame = ttk.Frame(self._main_frame)
        self.__bottom_frame.pack(fill=NONE, side=BOTTOM, padx=10, pady=10)

        self.__left_bottom_frame = ttk.Frame(self.__bottom_frame)
        self.__left_bottom_frame.pack(fill=NONE, side=LEFT, padx=5, pady=5)

        self.__right_bottom_frame = ttk.Frame(self.__bottom_frame)
        self.__right_bottom_frame.pack(fill=NONE, side=RIGHT, padx=5, pady=5)

        # cria um combobox para listar os itens selecionados
        self._selected_items_combo = ttk.Combobox(self._top_frame, state='readonly')
        self._selected_items_combo.config(values=self.__controller.fetch_selected_items())
        self._selected_items_combo_label = ttk.Label(self._top_frame, text='São os itens na comanda:')
        self._selected_items_combo.focus_set() # trás foco ao widget

        self._selected_items_combo_label.pack(padx=5, pady=5)
        self._selected_items_combo.pack(padx=5, pady=5)

        tooltip(self._selected_items_combo, 'Lista dos itens selecionados na comanda.')

        # cria botões para registrar a venda
        self._commit_sale_btn = ttk.Button(self.__left_bottom_frame, text='Confirmar', command=self.commit_sale, bootstyle='success', width=10) # type: ignore
        self.bind('<Control-f>', lambda e: self.commit_sale())
        self._cancel_sale_btn = ttk.Button(self.__left_bottom_frame, text='Cancelar', command=self.cancel_sale, bootstyle='danger', width=10) # type: ignore
        self.bind('<Control-c>', lambda e: self.cancel_sale())
        self._add_product_btn = ttk.Button(self.__right_bottom_frame, text='Adicionar produto', command=self.__controller.add_product, bootstyle='primary', width=20) # type: ignore
        self.bind('<Control-a>', lambda e: self.__controller.add_product())
        self._remove_product_btn = ttk.Button(self.__right_bottom_frame, text='Remover produto', command=self.remove_product, bootstyle='warning', width=20) # type: ignore
        self.bind('<Control-r>', lambda e: self.remove_product())

        self._commit_sale_btn.pack(side=TOP, padx=5, pady=5)
        self._cancel_sale_btn.pack(side=TOP, padx=5, pady=5)
        self._add_product_btn.pack(side=BOTTOM, padx=5, pady=5)
        self._remove_product_btn.pack(side=BOTTOM, padx=5, pady=5)

        tooltip(self._commit_sale_btn, '(Ctrl+F) Registrar a comanda no banco de dados.')
        tooltip(self._cancel_sale_btn, '(Ctrl+C) Cancelar a comanda.')
        tooltip(self._add_product_btn, '(Ctrl+A) Adicionar um produto à comanda.')
        tooltip(self._remove_product_btn, '(Ctrl+R) Remover um produto da comanda.')

    def on_close(self):
        if not self.__on_close:
            self.__on_close = True
            
            if msgbox.yesno('Deseja cancelar a comanda?', 'Cancelar comanda') == 'Sim':
                self.__parent_ctrl.order_ctrl = None

                self.__controller.on_close()
            else:
                self.__on_close = False

    def on_escape(self):
        self.on_close()

    def cancel_sale(self):
        self.on_close()

    def commit_sale(self):
        res = self.__controller.commit_sale()

        if res > 0.0:
            msgbox.show_info(f'Comanda deferida no valor de R${res}', 'Sucesso')

            self.__parent_ctrl.order_ctrl = None

            self.__controller.on_close()
        elif res < 0.0:
            msgbox.show_error('Não há estoque disponível para finalizar a comanda.', 'Erro')

            msgbox.show_warning('A comanda permanece indeferida.', 'Aviso')
        elif res == 0.0:
            msgbox.show_warning('A comanda está vazia.', 'Aviso')

    def remove_product(self):
        item_name = ''

        if self._selected_items_combo.get():
            item_name = self._selected_items_combo.get().split(')', 1)[1].strip()

        if not item_name:
            msgbox.show_error('Um produto precisa ser selecionado.', 'Erro')
        else:
            if not self.__on_item_removal:
                self.__on_item_removal = True

                if msgbox.yesno('Deseja remover o item da comanda?', 'Remoção de item') == 'Sim':
                    res = self.__controller.remove_product()

                    if res == 0:
                        msgbox.show_info('O produto foi removido da comanda.', 'Sucesso')

                        self._selected_items_combo.config(values=self.__controller.fetch_selected_items())
                        self._selected_items_combo.set('')
                    else:
                        msgbox.show_error('O produto não existe na comanda. A remoção do produto falhou.', 'Erro')
                
                    self.__on_item_removal = False
                else:
                    self.__on_item_removal = False

class ProductView(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl

        self.title('Seleção de Produto')
        self.geometry('400x300')
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        # observers
        alpha_validator = self.register(validate_alpha)
        number_validator = self.register(validate_number)

        # cria um frame para o conteúdo principal
        self._main_frame = ttk.Frame(self)
        self._main_frame.pack(fill=BOTH, expand=True)

        # cria um frame superior
        self._top_frame = ttk.Frame(self._main_frame)
        self._top_frame.pack(fill=X, side=TOP, padx=10, pady=10)

        # cria um frame inferior (para os botões)
        self.__bottom_frame = ttk.Frame(self._main_frame)
        self.__bottom_frame.pack(fill=X, side=BOTTOM, padx=10, pady=10)

        # adiciona um rótulo ao frame principal
        self.__main_label = ttk.Label(self._top_frame, text='Adicionar produto à comanda...', font=('Arial', 12))
        self.__main_label.pack(pady=20)

        self._item_name_combo = ttk.Combobox(self._top_frame, width=20, validate='focus', validatecommand=(alpha_validator, '%P'))
        self._item_name_combo.config(values=self.__controller.fetch_item_names())
        self._item_name_combo_label = ttk.Label(self._top_frame, text='Selecione o item:', font=('Arial', 10, 'bold'))
        self._item_name_combo.focus_set() # trás foco ao widget
        self._item_qty_spin = ttk.Spinbox(self._top_frame, from_=1, to=999, width=5, validate='focus', validatecommand=(number_validator, '%P'))
        self._item_qty_spin_label = ttk.Label(self._top_frame, text='Quantidade:', font=('Arial', 10, 'bold'))

        self._confirm_btn = ttk.Button(self.__bottom_frame, text='Adicionar', command=self.confirm_product, bootstyle='success', width=10) # type: ignore
        self.bind('<Control-a>', lambda e: self.confirm_product())
        self._cancel_btn = ttk.Button(self.__bottom_frame, text='Cancelar', command=self.cancel_product, bootstyle='danger', width=10) # type: ignore
        self.bind('<Control-c>', lambda e: self.cancel_product())

        self._item_name_combo_label.pack(pady=5)
        self._item_name_combo.pack(pady=5)
        self._item_qty_spin_label.pack(pady=5)
        self._item_qty_spin.pack(pady=5)
        
        self._confirm_btn.pack(side=LEFT, pady=10)
        self._cancel_btn.pack(side=RIGHT, pady=5)

        tooltip(self._item_name_combo, 'Selecione o item a ser adicionado à comanda.')
        tooltip(self._item_qty_spin, 'Informe a quantidade do item a ser adicionado à comanda.')
        tooltip(self._confirm_btn, '(Ctrl+A) Adicionar o item selecionado à comanda.')
        tooltip(self._cancel_btn, '(Ctrl+C) Cancelar a adição do produto à comanda.')

    def on_close(self):
        self.__parent_ctrl.product_ctrl = None
        self.destroy()

    def confirm_product(self):
        item_name = self._item_name_combo.get()
        item_qty = self._item_qty_spin.get()

        flag = True

        # valida os campos de entrada
        if not item_name or not item_qty:
            msgbox.show_error('Todos os campos obrigatórios devem ser preenchidos.', 'Erro')
        
            flag = False

        if flag and not validate_alpha(item_name):
            msgbox.show_error('O nome do item deve conter apenas letras e ter no máximo 30 caracteres.', 'Erro')

            flag = False
        
        if flag and not validate_number(item_qty):
            msgbox.show_error('A quantidade deve ser um número inteiro entre 0 e 999.', 'Erro')

            flag = False

        if flag:
            res = self.__controller.confirm_product()

            if res == 0:
                msgbox.show_info('Item adicionado na comanda.', 'Sucesso')

                # atualiza a combobox de itens selecionados na janela mãe (revisar /!\)
                self.__parent_ctrl._view._selected_items_combo.config(values=self.__parent_ctrl.fetch_selected_items())

                self.on_close()
            elif res == 1:
                msgbox.show_error('O item não existe no banco de dados.')

                flag = False
        if not flag:
            msgbox.show_error('A seleção do produto falhou.', 'Erro')

    def cancel_product(self):
        self.on_close()