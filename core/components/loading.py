import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import time
'''
    O módulo time fornece várias funções relacionadas ao tempo.
'''

class LoadingDialog(ttk.Toplevel):
    '''
        Janela modal simples de carregamento com barra indeterminada.
    '''

    def __init__(self, parent, message, mode, bootstyle, x, y):
        super().__init__(parent)
        self.title('Carregamento')
        self.geometry('300x100')
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.geometry(f'+{x}+{y}')

        self.protocol("WM_DELETE_WINDOW", lambda: None) # impede o usuário de fechar o widget

        ttk.Label(self, text=message, bootstyle=f'{bootstyle}').pack(padx=10, pady=10)
        self.bar = ttk.Progressbar(self, mode=mode, bootstyle=bootstyle)
        self.bar.pack(fill='x', padx=10, pady=10)
        self.bar.start(20)

    def close(self):
        self.bar.stop()
        self.destroy()
