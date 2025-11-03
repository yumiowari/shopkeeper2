import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox as msgbox
from ttkbootstrap.tooltip import ToolTip as tp
from ttkbootstrap.scrolled import ScrolledFrame
'''
    O módulo ttkbootstrap oferece uma extensão para o tkinter que permite
    temas modernos de estilo simples sob demanda inspirados no Bootstrap.
'''

from datetime import date
'''
    O módulo datetime oferece classes para manipulação de data e hora.
'''

from core.components.loading import LoadingDialog
"""
    Janela modal simples de carregamento com barra indeterminada.
"""

def validate_number(x) -> bool:
    '''
        Valida se o input é número inteiro até 999.
    '''
    if x == '':
        return True
    return x.isdigit() and int(x) <= 999

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
        self.place_window_center()

        self.update_idletasks()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()

        # coordenadas (x, y) para posicionar os Dialogs
        self.__x = x0 + w // 6
        self.__y = y0 + h // 6

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        number_validator = self.register(validate_number)

        '''
            Frame Principal
        '''
        self._main_frame = ttk.Frame(self)
        self._main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.__main_label = ttk.Label(self._main_frame, text='Insira as quantidades dos produtos...', font=('Arial', 12, 'bold'))
        self.__main_label.pack(padx=10, pady=10)

        self._scroll_frame = ScrolledFrame(self._main_frame, autohide=True)
        self._scroll_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self._button_frame = ttk.Frame(self._main_frame)
        self._button_frame.pack(side=BOTTOM, padx=10, pady=10)

        stock = self.__controller.fetch_product_names()
        self.__options = {}

        columns_per_row = 3
        row = 0
        column = 0

        for c in range(columns_per_row):
            self._scroll_frame.columnconfigure(c, weight=1)

        for product in stock:
            short_name = product[:15] # pega apenas o primeiros 15 caracteres

            option = ttk.Labelframe(self._scroll_frame, text=short_name)

            option.grid(row=row, column=column, padx=10, pady=10)

            spinbox = ttk.Spinbox(option, width=5, from_=0, to=999, validate='focus', validatecommand=(number_validator, '%P'))

            spinbox.pack(padx=10, pady=10)

            self.__options[product] = {
                "frame": option,
                "qty": spinbox
            }

            column += 1
            if column >= columns_per_row:
                column = 0
                row += 1

        self.__confirm_btn = ttk.Button(self._button_frame, text='Confirmar', command=self.commit_order, bootstyle='success', width=10)
        self.bind('<Return>', lambda e: self.commit_order())
        self.__cancel_btn = ttk.Button(self._button_frame, text='Cancelar', command=self.cancel_order, bootstyle='danger', width=10)
        self.bind('<Escape>', lambda e: self.cancel_order())

        self.__confirm_btn.pack(side=LEFT, padx=10, pady=10)
        self.__cancel_btn.pack(side=RIGHT, padx=10, pady=10)

        tp(self.__confirm_btn, 'Confirma o cadastro da comanda.', bootstyle=(SUCCESS, INVERSE))
        tp(self.__cancel_btn, 'Cancela o cadastro da comanda.', bootstyle=(DANGER, INVERSE))

    def on_close(self):
        if not self.__on_close:
            self.__on_close = True
            
            if msgbox.yesno('Deseja cancelar a comanda?', 'Cancelar comanda', parent=self, position=(self.__x, self.__y)) == 'Sim':
                self.__parent_ctrl.create_order_ctrl = None

                self.__controller.on_close()
            else:
                self.__on_close = False

    def commit_order(self):
        order = []

        for product in self.__options:
            product_name = product.cget('text')
            product_qty = product.qty.get()

            if not product_qty == '' and (not product_qty.isdigit() or int(product_qty) < 0):
                msgbox.show_error(f"'{product_qty}' não é uma quantidade válida.", 'Erro', parent=self, position=(self.__x, self.__y))

                return

            if product_qty == '' or product_qty == 0:
                continue

            order.append({'name': product_name, 'qty': product_qty})

        if not order:
            msgbox.show_warning('Pelo menos um produto precisa ser selecionado.\nNenhuma alteração foi feita.', 'Aviso', parent=self, position=(self.__x, self.__y))

        loading = LoadingDialog(self, message='Deferindo comanda...', mode='indeterminate', bootstyle='primary', x=self.__x, y=self.__y)

        loading.update()

        value = self.__controller.commit_order(order)

        self.after(500, loading.close)

        if value == 0.0:
            msgbox.show_error('Não há estoque disponível para finalizar a comanda.', 'Erro', parent=self, position=(self.__x, self.__y))
        elif value < 0.0:
            msgbox.show_error('Algum produto selecionado é inválido ou foi excluído.', 'Erro', parent=self, position=(self.__x, self.__y))
        elif value > 0.0:
            msgbox.show_info(f'Comanda deferida com valor de R${value}', 'Sucesso', parent=self, position=(self.__x, self.__y))

            self.__parent_ctrl._create_order_ctrl = None

            self.__controller.on_close()

    def cancel_order(self):
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
        self.place_window_center()

        self.update_idletasks()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()

        # coordenadas (x, y) para posicionar os Dialogs
        self.__x = x0 + w // 4
        self.__y = y0 + h // 4

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
            bootstyle='primary'
        )
        self._date_entry.configure(state='readonly')
        self._date_entry_label = ttk.Label(self._main_frame, text='Selecione a data:', font=('Arial', 10, 'bold'))
        self._timestamp_combo = ttk.Combobox(self._main_frame, width=20, state='readonly', validate='focus')
        self._timestamp_combo_label = ttk.Label(self._main_frame, text='Selecione o timestamp:', font=('Arial', 10, 'bold'))

        '''
            Botões
        '''
        self._confirm_btn = ttk.Button(self._main_frame, text='Confirmar', command=self.confirm_selected_date, bootstyle='primary', width=10)
        self._confer_btn = ttk.Button(self._main_frame, text='Consultar', command=self.confer_selected_order, bootstyle='success', width=10)

        self._date_entry_label.pack(pady=5)
        self._date_entry.pack(pady=5)
        self._confirm_btn.pack(pady=10)
        self._timestamp_combo_label.pack(pady=5)
        self._timestamp_combo.pack(pady=5)
        self._confer_btn.pack(pady=10)

        tp(self._date_entry, 'Em que dia a comanda foi deferida?', bootstyle=(PRIMARY, INVERSE))
        tp(self._confirm_btn, 'Confirmar a data selecionada.', bootstyle=(PRIMARY, INVERSE))
        tp(self._timestamp_combo, 'Em que horário a comanda foi deferida?', bootstyle=(PRIMARY, INVERSE))
        tp(self._confer_btn, 'Consultar a comanda selecionada.', bootstyle=(SUCCESS, INVERSE))

    def on_close(self):
        self.__parent_ctrl._confer_order_ctrl = None
        self.destroy()

    def on_escape(self):
        self.on_close()

    def confirm_selected_date(self):
        order_list = self.__controller.fetch_order_list()

        if order_list == []:
            msgbox.show_warning('Nenhuma comanda foi vendida na data selecionada.', 'Aviso', parent=self, position=(self.__x, self.__y))
        else:
            timestamps = []

            for order in order_list:
                timestamps.append(order.timestamp)

            timestamps = sorted(order.timestamp for order in order_list) # ordena de acordo com o timestamp

            self._timestamp_combo.config(values=timestamps)

    def confer_selected_order(self):
        selected_timestamp = self._timestamp_combo.get()

        if not selected_timestamp:
            msgbox.show_warning('Um timestamp válido precisa ser selecionado.', 'Aviso', parent=self, position=(self.__x, self.__y))
        else:
            order = self.__controller.fetch_order()
            stock = self.__controller.fetch_stock()

            if order == None:
                msgbox.show_error('A comanda selecionada é inválida ou foi excluída.', 'Erro', parent=self, position=(self.__x, self.__y))
            else:
                output = f'É a comanda: {order.timestamp}\n\n'
                
                for sale in order.sales:
                    for product in stock:
                        if sale.product_id == product.id:
                            output += f'{product.name} - {sale.qty} - R$ {sale.value}\n'

                            break

                output += f'\nTotal: R${order.value}'

                msgbox.show_info(output, 'Sucesso', parent=self, position=(self.__x, self.__y))