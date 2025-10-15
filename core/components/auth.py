import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox as msgbox
from ttkbootstrap.tooltip import ToolTip as tp

import core.components.SGBD as SGBD
'''
    SGBD implementa funções para manipulação do banco de dados.
'''

class AuthDialog(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Autenticação')
        self.geometry('400x300')
        self.resizable(False, False)
        self.place_window_center()
        self.transient(parent)
        self.grab_set()

        self.update_idletasks()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()

        # coordenadas (x, y) para posicionar os Dialogs
        self.__x = x0 + w // 6
        self.__y = y0 + h // 6

        self.access_granted = False # flag de autenticação

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.bind('<Escape>', lambda e: self.on_escape())

        '''
            Frame Principal
        '''
        self._main_frame = ttk.Frame(self)
        self._main_frame.pack(fill=BOTH, expand=True)

        self.__main_label = ttk.Label(self._main_frame, text='Acesso restrito.', font=('Arial', 12, 'bold'))
        self.__main_label.pack(pady=20)

        '''
            Campos de Entrada
        '''
        self._username_entry = ttk.Entry(self._main_frame, width=20)
        self._username_entry_label = ttk.Label(self._main_frame, text='Nome de usuário:', font=('Arial', 10, 'bold'))
        self._password_entry = ttk.Entry(self._main_frame, width=20, show='*')
        self._password_entry_label = ttk.Label(self._main_frame, text='Senha:', font=('Arial', 10, 'bold'))

        self._confirm_btn = ttk.Button(self._main_frame, text='Confirmar', command=self.validate_user, bootstyle='success', width=10)

        self._username_entry_label.pack(pady=5)
        self._username_entry.pack(pady=5)
        self._password_entry_label.pack(pady=5)
        self._password_entry.pack(pady=5)
        self._confirm_btn.pack(pady=10)

        tp(self._username_entry, 'Qual o nome de usuário do administrador?', bootstyle=(PRIMARY, INVERSE))
        tp(self._password_entry, 'Qual a senha do administrador?', bootstyle=(PRIMARY, INVERSE))
        tp(self._confirm_btn, 'Confirmar as credenciais de administrador.', bootstyle=(SUCCESS, INVERSE))

    def on_close(self):
        self.destroy()

    def on_escape(self):
        self.on_close()

    def validate_user(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        if not username or not password:
            msgbox.show_error('Todos os campos obrigatórios devem ser preenchidos.', 'Erro', parent=self, position=(self.__x, self.__y))

            self.destroy()

            return

        model = AuthModel()

        if model.validate_credentials(username, password):
            self.access_granted = True
        else:
            msgbox.show_error('Credenciais inválidas.', 'Erro', parent=self, position=(self.__x, self.__y))

        self.destroy()

class AuthModel:
    def __init__(self):
        self.__credentials = SGBD.fetch_credentials()

    def validate_credentials(self, username, password):
        if username == self.__credentials['username'] and password == self.__credentials['password']:
            return True
        else:
            return False
        