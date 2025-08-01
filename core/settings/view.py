import ttkbootstrap as ttk
from ttkbootstrap.constants import * # type: ignore
from ttkbootstrap.dialogs import Messagebox as msgbox
from ttkbootstrap.tooltip import ToolTip as tp
'''
    O módulo ttkbootstrap oferece uma extensão para o tkinter que permite
    temas modernos de estilo simples sob demanda inspirados no Bootstrap.
'''

'''
    Janela de Preferências

    Disponibiliza opções para personalização da aplicação.
'''
class View(ttk.Toplevel):
    def __init__(self, controller, parent_ctrl):
        super().__init__()
        self.__controller = controller
        self.__parent_ctrl = parent_ctrl

        self.title('Preferências')
        self.geometry('400x300')
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.bind('<Escape>', lambda e: self.on_escape())

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

        self.__main_label = ttk.Label(self._top_frame, text='Alterar preferências da aplicação...', font=('Arial', 12))
        self.__main_label.pack(pady=20)

        '''
            Combobox de temas disponíveis
        '''
        themes = ['cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean', 'solar', 'superhero', 'darkly', 'cyborg', 'vapor']
        self._theme_name_combo = ttk.Combobox(self._top_frame, width=20, state='readonly')
        self._theme_name_combo.config(values=themes)
        self._theme_name_combo_label = ttk.Label(self._top_frame, text='Selecione o tema:', font=('Arial', 10, 'bold'))

        self._theme_name_combo_label.pack(padx=5, pady=5)
        self._theme_name_combo.pack(padx=5, pady=5)

        '''
            Botões
        '''
        self._confirm_btn = ttk.Button(self.__bottom_frame, text='Confirmar', command=self.confirm_theme, bootstyle='success', width=10) # type: ignore

        self._confirm_btn.pack(padx=5, pady=5)

    def on_close(self):
        self.__parent_ctrl._settings_ctrl = None
        self.destroy()

    def on_escape(self):
        self.on_close()

    def confirm_theme(self):
        theme_name = self._theme_name_combo.get()

        if not theme_name:
            msgbox.show_error('Um tema precisa ser selecionado.', 'Erro')
        else:
            self.__controller.confirm_theme()