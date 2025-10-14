import core.components.SGBD as SGBD
'''
    SGBD implementa funções para manipulação do banco de dados.
'''

import csv
'''
    csv provê funções para manipulação de arquivos CSV (valores separados por vírgula).
'''

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
'''
    ReportLab é uma biblioteca Python open-source usada para gerar documentos PDF.
'''

from datetime import datetime
'''
    O módulo datetime oferece classes para manipulação de data e hora.
'''

import os
'''
    os provê uma forma portátil de usar operações dependentes do sistema operacional.
'''

import pickle as pkl
'''
    O módulo pickle em Python permite serializar e desserializar objetos Python,
    transformando-os em uma sequência de bytes que pode ser armazenada em um arquivo.
'''

class Model:
    def __init__(self):
        self.__stock = []

        # "current order"
        self.__curr_order = [] # list of sales

    '''
        Imprime o relatório do estoque no arquivo PDF

        Retorna...
            0 - Sucesso;
            1 - Estoque vazio.
    '''
    def make_stock_report(self):
        table = [
            ['ID', 'Produto', 'Custo', 'Preço', 'Quantidade']
        ]

        self.__stock = SGBD.fetch_stock()

        self.__stock.sort(key=lambda s: s.id) # ordena a lista pelo identificador

        if self.__stock == []:
            return 1

        for product in self.__stock:
            row = []

            row.append(product.id)
            row.append(product.name)
            row.append(f"R$ {product.cost:.2f}".replace('.', ','))
            row.append(f"R$ {product.price:.2f}".replace('.', ','))
            row.append(product.qty)

            table.append(row)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # persiste o arquivo CSV
        with open('data/stock ' + timestamp + '.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(table)

        # cria o documento PDF
        pdf = SimpleDocTemplate('stock ' + timestamp + '.pdf', pagesize=A4, title='Relatório do Estoque: ' + timestamp)
        elements = []

        # converte a lista para um Flowable Table do ReportLab
        flowable_table = Table(table)

        # adiciona estilo
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        flowable_table.setStyle(style)

        elements.append(flowable_table)

        # gera o arquivo PDF
        pdf.build(elements)

        return 0
    
    '''
        Imprime o relatório de Fechamento de Caixa

        Retorna...
            Valores positivos - Sucesso;
            Valores nulos - Nenhuma comanda foi cadastrada na data selecionada.
    '''
    def make_order_report(self, selected_date):
        report = {
            'revenue': 0.0,
            'profit': 0.0
        }

        # recupera o estoque para calcular o lucro para cada produto
        self.__stock = SGBD.fetch_stock()

        for folder_name in os.listdir('data'):
            folder_path = os.path.join('data', folder_name)

            if os.path.isdir(folder_path):
                # verifica se o nome da pasta começa com a data selecionada
                if folder_name.startswith(selected_date.strftime('%Y-%m-%d')):
                    file_path = os.path.join(folder_path, 'order.pkl')
                    
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            comm_order = pkl.load(file)

                            # incrementa a receita
                            report['revenue'] += float(comm_order.value)

                            # incrementa o lucro
                            for sale in comm_order.sales:
                                for product in self.__stock:
                                    if sale.product_id == product.id:
                                        # LUCRO += (PREÇO - CUSTO) * QUANTIDADE
                                        report['profit'] += float(float(float(product.price) - float(product.cost)) * int(sale.qty))

                                        break

        return report
    
    '''
        Função para carregar o tema persistido na memória
    '''
    def fetch_curr_theme(self):
        try:
            with open('data/curr_theme.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return 'litera' # retorna o tema padrão (litera)