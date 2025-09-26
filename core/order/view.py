import ttkbootstrap as ttk
from ttkbootstrap.constants import * # type: ignore
from ttkbootstrap.dialogs import Messagebox as msgbox
from ttkbootstrap.tooltip import ToolTip as tp
'''
    O módulo ttkbootstrap oferece uma extensão para o tkinter que permite
    temas modernos de estilo simples sob demanda inspirados no Bootstrap.
'''

from datetime import date
'''
    O módulo datetime oferece classes para manipulação de data e hora.
'''

def validate_alpha(x) -> bool:
    '''
        Valida se o input é alfabético de até 30 caracteres.
    '''
    return (x == '' or not x.isdigit()) and len(x) <= 30

def validate_number(x) -> bool:
    '''
        Valida se o input é número inteiro entre 1 e 999.
    '''
    if x == '':
        return True
    return x.isdigit() and int(x) <= 999 and int(x) >= 1

'''
    Janela para cadastro de Comanda

    Disponibiliza a UI para gerenciar a comanda.
'''
class CreateOrderView(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl
        self.__on_close = False
        self.__on_product_removal = False

        self.title('Cadastro de Comanda')
        self.geometry('600x450')
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.bind('<Escape>', lambda e: self.on_escape())

        '''
            Frame Principal
        '''
        self._main_frame = ttk.Frame(self)
        self._main_frame.pack(fill=BOTH, expand=True)
        # X - Preenche a largura
        # Y - Preenche a altura
        # BOTH - Preenche ambos
        # NONE - Não preenche nada

        self.__main_label = ttk.Label(self._main_frame, text='Cadastrar comanda...', font=('Arial', 12))
        self.__main_label.pack(pady=20)

        # Frame Superior
        self._top_frame = ttk.Frame(self._main_frame)
        self._top_frame.pack(fill=NONE, side=TOP, padx=10, pady=10)

        # Frame Inferior (para os botões)
        self.__bottom_frame = ttk.Frame(self._main_frame)
        self.__bottom_frame.pack(fill=NONE, side=BOTTOM, padx=10, pady=10)

        self.__left_bottom_frame = ttk.Frame(self.__bottom_frame)
        self.__left_bottom_frame.pack(fill=NONE, side=LEFT, padx=5, pady=5)

        self.__right_bottom_frame = ttk.Frame(self.__bottom_frame)
        self.__right_bottom_frame.pack(fill=NONE, side=RIGHT, padx=5, pady=5)

        # Combobox para listar os itens selecionados
        self._selected_products_combo = ttk.Combobox(self._top_frame, width=20, state='readonly')
        self._selected_products_combo.config(values=self.__controller.fetch_selected_products())
        self._selected_products_combo_label = ttk.Label(self._top_frame, text='São os itens na comanda:')
        self._selected_products_combo.focus_set() # trás foco ao widget

        self._selected_products_combo_label.pack(padx=5, pady=5)
        self._selected_products_combo.pack(padx=5, pady=5)

        tp(self._selected_products_combo, 'Lista dos itens selecionados na comanda.')

        '''
            Botões
        '''
        self._commit_sale_btn = ttk.Button(self.__left_bottom_frame, text='Confirmar', command=self.commit_sale, bootstyle='success', width=10) # type: ignore
        self.bind('<Control-f>', lambda e: self.commit_sale())
        self.bind('<Control-F>', lambda e: self.commit_sale())
        self._cancel_sale_btn = ttk.Button(self.__left_bottom_frame, text='Cancelar', command=self.cancel_sale, bootstyle='danger', width=10) # type: ignore
        self.bind('<Control-c>', lambda e: self.cancel_sale())
        self.bind('<Control-C>', lambda e: self.cancel_sale())
        self._add_product_btn = ttk.Button(self.__right_bottom_frame, text='Adicionar produto', command=self.__controller.add_product, bootstyle='primary', width=20) # type: ignore
        self.bind('<Control-a>', lambda e: self.__controller.add_product())
        self.bind('<Control-A>', lambda e: self.__controller.add_product())
        self._remove_product_btn = ttk.Button(self.__right_bottom_frame, text='Remover produto', command=self.remove_product, bootstyle='warning', width=20) # type: ignore
        self.bind('<Control-r>', lambda e: self.remove_product())
        self.bind('<Control-R>', lambda e: self.remove_product())

        self._commit_sale_btn.pack(side=TOP, padx=5, pady=5)
        self._cancel_sale_btn.pack(side=TOP, padx=5, pady=5)
        self._add_product_btn.pack(side=BOTTOM, padx=5, pady=5)
        self._remove_product_btn.pack(side=BOTTOM, padx=5, pady=5)

        tp(self._commit_sale_btn, '(Ctrl+F) Registrar a comanda no banco de dados.')
        tp(self._cancel_sale_btn, '(Ctrl+C) Cancelar a comanda.')
        tp(self._add_product_btn, '(Ctrl+A) Adicionar um produto à comanda.')
        tp(self._remove_product_btn, '(Ctrl+R) Remover um produto da comanda.')

    def on_close(self):
        if not self.__on_close:
            self.__on_close = True
            
            if msgbox.yesno('Deseja cancelar a comanda?', 'Cancelar comanda') == 'Sim':
                self.__parent_ctrl._create_order_ctrl = None

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

            self.__parent_ctrl._create_order_ctrl = None

            self.__controller.on_close()
        elif res < 0.0:
            msgbox.show_error('Não há estoque disponível para finalizar a comanda.', 'Erro')

            msgbox.show_warning('A comanda permanece indeferida.', 'Aviso')
        elif res == 0.0:
            msgbox.show_warning('A comanda está vazia.', 'Aviso')

    def remove_product(self):
        product_name = ''

        if self._selected_products_combo.get():
            product_name = self._selected_products_combo.get().split(')', 1)[1].strip()

        if not product_name:
            msgbox.show_error('Um produto precisa ser selecionado.', 'Erro')
        else:
            if not self.__on_product_removal:
                self.__on_product_removal = True

                if msgbox.yesno('Deseja remover o produto da comanda?', 'Remoção de produto') == 'Sim':
                    res = self.__controller.remove_product()

                    if res == 0:
                        msgbox.show_info('O produto foi removido da comanda.', 'Sucesso')

                        self._selected_products_combo.config(values=self.__controller.fetch_selected_products())
                        self._selected_products_combo.set('')
                    else:
                        msgbox.show_error('O produto não existe na comanda. A remoção do produto falhou.', 'Erro')
                
                    self.__on_product_removal = False
                else:
                    self.__on_product_removal = False

'''
    Janela para seleção de Produto

    Disponibiliza a UI para adicionar itens à comanda.
'''
class SelectProductView(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl

        self.title('Seleção de Produto')
        self.geometry('400x300')
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.bind('<Escape>', lambda e: self.on_escape())

        '''
            Observers

            Funções associadas a algum campo de entrada para validar o conteúdo digitado.
        '''
        alpha_validator = self.register(validate_alpha)
        number_validator = self.register(validate_number)

        '''
            Frame Principal
        '''
        self._main_frame = ttk.Frame(self)
        self._main_frame.pack(fill=BOTH, expand=True)

        # Frame Superior
        self._top_frame = ttk.Frame(self._main_frame)
        self._top_frame.pack(fill=X, side=TOP, padx=10, pady=10)

        # Frame Inferior (para os botões)
        self.__bottom_frame = ttk.Frame(self._main_frame)
        self.__bottom_frame.pack(fill=X, side=BOTTOM, padx=10, pady=10)

        self.__main_label = ttk.Label(self._top_frame, text='Adicionar produto à comanda...', font=('Arial', 12))
        self.__main_label.pack(pady=20)

        '''
            Campos de Entrada
        '''
        self._product_name_combo = ttk.Combobox(self._top_frame, width=20, validate='focus', validatecommand=(alpha_validator, '%P'))
        self._product_name_combo.config(values=self.__controller.fetch_product_names())
        self._product_name_combo_label = ttk.Label(self._top_frame, text='Selecione o produto:', font=('Arial', 10, 'bold'))
        self._product_name_combo.focus_set() # trás foco ao widget
        self._product_qty_spin = ttk.Spinbox(self._top_frame, from_=1, to=999, width=5, validate='focus', validatecommand=(number_validator, '%P'))
        self._product_qty_spin_label = ttk.Label(self._top_frame, text='Quantidade:', font=('Arial', 10, 'bold'))

        '''
            Botões
        '''
        self._confirm_btn = ttk.Button(self.__bottom_frame, text='Adicionar', command=self.confirm_product, bootstyle='success', width=10) # type: ignore
        self.bind('<Control-a>', lambda e: self.confirm_product())
        self.bind('<Control-A>', lambda e: self.confirm_product())
        self._cancel_btn = ttk.Button(self.__bottom_frame, text='Cancelar', command=self.cancel_product, bootstyle='danger', width=10) # type: ignore
        self.bind('<Control-c>', lambda e: self.cancel_product())
        self.bind('<Control-C>', lambda e: self.cancel_product())

        self._product_name_combo_label.pack(pady=5)
        self._product_name_combo.pack(pady=5)
        self._product_qty_spin_label.pack(pady=5)
        self._product_qty_spin.pack(pady=5)
        
        self._confirm_btn.pack(side=LEFT, pady=5)
        self._cancel_btn.pack(side=RIGHT, pady=5)

        tp(self._product_name_combo, 'Selecione o produto a ser adicionado à comanda.')
        tp(self._product_qty_spin, 'Informe a quantidade do produto a ser adicionado à comanda.')
        tp(self._confirm_btn, '(Ctrl+A) Adicionar o produto selecionado à comanda.')
        tp(self._cancel_btn, '(Ctrl+C) Cancelar a adição do produto à comanda.')

    def on_close(self):
        self.__parent_ctrl._select_product_ctrl = None
        self.destroy()

    def on_escape(self):
        self.on_close()

    def confirm_product(self):
        product_name = self._product_name_combo.get()
        product_qty = self._product_qty_spin.get()

        flag = True

        # valida os campos de entrada
        if not product_name or not product_qty:
            msgbox.show_error('Todos os campos obrigatórios devem ser preenchidos.', 'Erro')
        
            flag = False

        if flag and not validate_alpha(product_name):
            msgbox.show_error('O nome do produto deve conter apenas letras e ter no máximo 30 caracteres.', 'Erro')

            flag = False
        
        if flag and not validate_number(product_qty):
            msgbox.show_error('A quantidade deve ser um número inteiro entre 0 e 999.', 'Erro')

            flag = False

        if flag:
            res = self.__controller.confirm_product()

            if res == 0:
                msgbox.show_info('produto adicionado na comanda.', 'Sucesso')

                # atualiza a combobox de itens selecionados na janela mãe
                self.__parent_ctrl._view._selected_products_combo.config(values=self.__parent_ctrl.fetch_selected_products())

                self.on_close()
            elif res == 1:
                msgbox.show_error('O produto não existe no banco de dados.')

                flag = False
        if not flag:
            msgbox.show_error('A seleção do produto falhou.', 'Erro')

    def cancel_product(self):
        self.on_close()

'''
    Janela para consulta de Comanda

    Disponibiliza a UI para consultar as comandas deferidas.
'''
class ConferOrderView(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl

        self.title('Consulta de Comanda')
        self.geometry('600x450')
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.bind('<Escape>', lambda e: self.on_escape())

        '''
            Frame Principal
        '''
        self._main_frame = ttk.Frame(self)
        self._main_frame.pack(fill=BOTH, expand=True)

        self.__main_label = ttk.Label(self._main_frame, text='Consultar comanda deferida...', font=('Arial', 12))
        self.__main_label.pack(pady=20)

        '''
            Campos de Entrada
        '''
        self._date_entry = ttk.DateEntry(
            self._main_frame,
            firstweekday=6, # domingo
            startdate=date.today(),
            bootstyle='info'
        )
        self._date_entry.configure(state='readonly')
        self._date_entry_label = ttk.Label(self._main_frame, text='Selecione a data:', font=('Arial', 10, 'bold'))
        self._timestamp_combo = ttk.Combobox(self._main_frame, width=20, state='readonly', validate='focus')
        self._timestamp_combo_label = ttk.Label(self._main_frame, text='Selecione o timestamp:', font=('Arial', 10, 'bold'))

        '''
            Botões
        '''
        self._confirm_btn = ttk.Button(self._main_frame, text='Confirmar', command=self.confirm_selected_date, bootstyle='info', width=10) # type: ignore
        self._confer_btn = ttk.Button(self._main_frame, text='Consultar', command=self.confer_selected_order, bootstyle='success', width=10) # type: ignore

        self._date_entry_label.pack(pady=5)
        self._date_entry.pack(pady=5)
        self._confirm_btn.pack(pady=10)
        self._timestamp_combo_label.pack(pady=5)
        self._timestamp_combo.pack(pady=5)
        self._confer_btn.pack(pady=10)

        tp(self._date_entry, 'Em que dia a comanda foi deferida?')
        tp(self._confirm_btn, 'Confirmar a data selecionada.')
        tp(self._timestamp_combo, 'Em que horário a comanda foi deferida?')
        tp(self._confer_btn, 'Consultar a comanda selecionada.')

    def on_close(self):
        self.__parent_ctrl._confer_order_ctrl = None
        self.destroy()

    def on_escape(self):
        self.on_close()

    def confirm_selected_date(self):
        order_list = self.__controller.fetch_order_list()

        if order_list == []:
            msgbox.show_warning('Nenhuma comanda foi vendida na data selecionada.', 'Aviso')
        else:
            timestamps = []

            for order in order_list:
                timestamps.append(order.timestamp)

            self._timestamp_combo.config(values=timestamps)

    def confer_selected_order(self):
        selected_timestamp = self._timestamp_combo.get()

        if not selected_timestamp:
            msgbox.show_warning('Um timestamp válido precisa ser selecionado.', 'Aviso')
        else:
            order = self.__controller.fetch_order()

            if order == {}:
                msgbox.show_error('A comanda selecionada é inválida ou foi excluída.', 'Erro')
            else:
                output = f'É a comanda: {order.timestamp}\n\n'
                for sale in order.sales:
                    output += f'{sale.product_id} - {sale.qty} - R$ {sale.value}\n'
                output += f'\nTotal: R${order.value}'

                msgbox.show_info(output, 'Sucesso')