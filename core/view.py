import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox as msgbox
from ttkbootstrap.dialogs import DatePickerDialog
from ttkbootstrap.tooltip import ToolTip as tp
from ttkbootstrap import Style
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

class View(ttk.Window):
    '''
        Classe para renderizar o conteúdo da janela principal (ttk.Window).

        Todas as demais janelas (ttk.Toplevel) são filhas da janela principal.

        Encerrar a janela principal implica em encerrar a aplicação.
    '''
    def __init__(self, controller):
        super().__init__()
        self.__controller = controller

        self.title('$hopkeeper')
        self.geometry('800x600')
        self.resizable(False, False)
        self.place_window_center()

        # atualiza o tema da janela
        Style().theme_use(self.__controller.fetch_curr_theme())

        # flags...
        self.__on_shutdown = False
        self.__on_stock_report = False
        # ...utilizadas para impedir a abertura de mais de uma janela toplevel do mesmo tipo

        self.protocol('WM_DELETE_WINDOW', self.shutdown)

        '''
            Frames

            "Frame" é um widget que atua como um contêiner para outros widgets,
            permitindo organizar a interface gráfica de forma estruturada.
        '''
        self.__main_frame = ttk.Frame(self)
        self.__top_frame = ttk.Frame(self.__main_frame)
        self.__bottom_frame = ttk.Frame(self.__main_frame)

        self.__main_frame.pack(fill=BOTH, expand=True)
        self.__top_frame.pack(fill=X, side=TOP, padx=10, pady=10)
        self.__bottom_frame.pack(fill=NONE, side=BOTTOM, padx=10, pady=10)
        # fill...
        # X - Preenche a largura
        # Y - Preenche a altura
        # BOTH - Preenche ambos
        # NONE - Não preenche nada

        '''
            Labels

            "Label" é usado para exibir texto ou imagens estáticas na interface gráfica.
        '''
        self.__main_label = ttk.Label(self.__top_frame, text='Seja bem-vindo ao $hopkeeper!', font=('Arial', 16))
        self.__main_label.pack(pady=20)

        '''
            Barra de Menu: Estrutura os módulos e funções da aplicação.
        '''
        self.__menu_bar = ttk.Menu(self)
        self.config(menu=self.__menu_bar)

        # Menu de Arquivo: Preferências e funções gerais da aplicação.
        self.__file_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__file_menu.add_command(label='Preferências', command=self.__controller.open_settings_window)
        self.__file_menu.add_separator()
        self.__file_menu.add_command(label='Sair', accelerator='Ctrl+Q', command=self.shutdown)
        self.bind_all('<Control-q>', lambda e: self.shutdown())
        self.bind_all('<Control-Q>', lambda e: self.shutdown())
        # bind_all() observa a hotkey em todas as janelas da aplicação.
        self.__menu_bar.add_cascade(label='Arquivo', menu=self.__file_menu)

        # Menu de Estoque
        self.__stock_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__stock_menu.add_command(label='Inventário', accelerator='Ctrl+I', command=self.__controller.open_stock_window)
        self.bind('<Control-i>', lambda e: self.__controller.open_stock_window())
        self.bind('<Control-I>', lambda e: self.__controller.open_stock_window())
        # bind() observa a hotkey apenas na janela de foco.
        self.__stock_menu.add_command(label='Entrada', accelerator='Ctrl+E', command=self.__controller.open_stock_entry_window)
        self.bind('<Control-e>', lambda e: self.__controller.open_stock_entry_window())
        self.bind('<Control-E>', lambda e: self.__controller.open_stock_entry_window())
        self.__stock_menu.add_separator()
        self.__stock_menu.add_command(label='Relatório', accelerator='Ctrl+Shift+I', command=self.make_stock_report)
        self.bind('<Control-Shift-I>', lambda e: self.make_stock_report())
        self.bind('<Control-Shift-i>', lambda e: self.make_stock_report())
        # /!\ deve considerar tanto a letra em minúsculo quanto em maíusculo para tratar quando CapsLock estiver pressionada
        self.__menu_bar.add_cascade(label='Estoque', menu=self.__stock_menu)

        # Menu de Caixa
        self.__sales_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__sales_menu.add_command(label='Cadastro de Comanda', accelerator='Ctrl+V', command=self.__controller.open_create_order_window)
        self.bind('<Control-v>', lambda e: self.__controller.open_create_order_window())
        self.bind('<Control-V>', lambda e: self.__controller.open_create_order_window())
        self.__sales_menu.add_command(label='Consulta de Comanda', command=self.__controller.open_confer_order_window)
        self.__sales_menu.add_separator()
        self.__sales_menu.add_command(label='Relatório', accelerator='Ctrl+Shift+V', command=self.make_order_report)
        self.bind('<Control-Shift-V>', lambda e: self.make_order_report())
        self.bind('<Control-Shift-v>', lambda e: self.make_order_report())
        self.__menu_bar.add_cascade(label='Caixa', menu=self.__sales_menu)

        # Menu de Ajuda 
        self.__help_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__help_menu.add_command(label='Sobre', command=self.__controller.open_about_window)
        self.__menu_bar.add_cascade(label='Ajuda', menu=self.__help_menu)

        # Menu de Créditos
        self.__credits_menu = ttk.Menu(self.__menu_bar, tearoff=0)
        self.__credits_menu.add_command(label='Créditos', command=self.__controller.open_credits_window)
        self.__menu_bar.add_cascade(label='Créditos', menu=self.__credits_menu)

        '''
            Botões de acesso rápido
        '''
        self.__order_btn = ttk.Button(self.__bottom_frame, text='Vender', command=self.__controller.open_create_order_window, bootstyle='success', width=10)
        self.__entry_btn = ttk.Button(self.__bottom_frame, text='Entrada', command=self.__controller.open_stock_entry_window, bootstyle='info', width=10)

        self.__order_btn.pack(side=LEFT, padx=10, pady=10)
        self.__entry_btn.pack(side=RIGHT, padx=10, pady=10)

        tp(self.__order_btn, '(Ctrl+V) Cadastrar uma comanda.', bootstyle=(SUCCESS, INVERSE))
        tp(self.__entry_btn, '(Ctrl+E) Cadastrar uma entrada/saída de produto.', bootstyle=(INFO, INVERSE))

        '''
            Rodapé
        '''
        self.__footer = ttk.Label(self, text='Copyright © 2025 Rafael Renó Corrêa | owariyumi@gmail.com', font=('Arial', 10), anchor='center')
        self.__footer.pack(side=BOTTOM, fill=X, pady=5)

    '''
        Função para imprimir o relatório de estoque em PDF.
    '''
    def make_stock_report(self):
        if not self.__on_stock_report:
            self.__on_stock_report = True

            if msgbox.yesno('Deseja imprimir o relatório do estoque?', 'Confirmação') == 'Sim':
                loading = LoadingDialog(self, message='Gerando relatório do comandas...')

                loading.update()

                feedback = self.__controller.make_stock_report()

                self.after(500, loading.close)  
            
                if feedback == 0:
                    msgbox.show_info('Relatório do estoque impresso no diretório raiz da aplicação.', 'Sucesso')
                elif feedback == 1:
                    msgbox.show_error('O inventário está vazio: Não existem itens disponíveis para impressão.', 'Erro')
            
                self.__on_stock_report = False
            else:
                self.__on_stock_report = False

    '''
        Fechamento de Caixa

        Função para imprimir o relatório de comandas.
    '''
    def make_order_report(self):
        self._dialog = DatePickerDialog(
            title='Seleção de data',
            firstweekday=6, # domingo
            startdate=date.today(),
            bootstyle='info'
        )

        if msgbox.yesno(f"Deseja imprimir o relatório do dia {self._dialog.date_selected.strftime('%d/%m/%Y')}?", 'Confirmação') == 'Sim':
            loading = LoadingDialog(self, message='Gerando relatório do comandas...')

            loading.update()

            report = self.__controller.make_order_report()

            self.after(500, loading.close)

            if report['revenue'] == 0.0 and report['profit'] == 0.0:
                msgbox.show_error('Nenhuma comanda foi cadastrada na data selecionada.', 'Erro')
            else:
                output = f'É o relatório do dia {self._dialog.date_selected.strftime('%d/%m/%Y')}:\n\n'
                output += 'Receita: R$ ' + str(report['revenue']) + '\n'
                output += 'Lucro: R$ ' + str(report['profit']) + '\n'

                msgbox.show_info(output, 'Sucesso')
        else:
            msgbox.show_warning('A impressão do relatório foi cancelada: Nenhum arquivo foi criado.', 'Aviso')
            
    '''
        Rotina de Encerramento Gracioso
    '''
    def shutdown(self):
        if not self.__on_shutdown:
            self.__on_shutdown = True
            
            if msgbox.yesno('Deseja encerrar a aplicação?', 'Confirmação') == 'Sim':
                self.__controller.shutdown()
            else:
                self.__on_shutdown = False