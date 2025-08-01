import ttkbootstrap as ttk
from ttkbootstrap.constants import * # type: ignore
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

    def on_close(self):
        self.__parent_ctrl._settings_ctrl = None
        self.destroy()

    def on_escape(self):
        self.on_close()