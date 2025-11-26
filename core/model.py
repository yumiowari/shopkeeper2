import core.components.db as db
'''
    db implementa funções para manipulação do banco de dados.
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
            caminho do PDF - Sucesso;
            caminho vazio - Estoque vazio.
    '''
    def make_stock_report(self):
        self.__stock = db.fetch_stock()

        if not self.__stock:
            return ''

        # ordena pelo nome da categoria e depois pelo produto
        self.__stock.sort(key=lambda s: (s.category, s.name))

        table = [['Categoria', 'Produto', 'ID', 'Custo', 'Preço', 'Quantidade']]

        for product in self.__stock:
            row = [
                product.category,
                product.name,
                product.id,
                f"R$ {product.cost:.2f}".replace('.', ','),
                f"R$ {product.price:.2f}".replace('.', ','),
                product.qty
            ]
            table.append(row)

        timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

        # Salva em arquivo CSV
        with open(f'data/stock {timestamp}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(table)

        path = f'data/stock {timestamp}.pdf'

        # Cria arquivo PDF
        pdf = SimpleDocTemplate(path, pagesize=A4, title='Relatório do Estoque: ' + timestamp)
        elements = []

        flowable_table = Table(table, repeatRows=1) # repete o cabeçalho em novas páginas

        # estilo
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # adiciona destaque para linhas de categoria (opcional)
        current_category = None
        for i, row in enumerate(table[1:], start=1):
            if row[0] != current_category:
                style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
                style.add('FONTNAME', (0, i), (-1, i), 'Helvetica-Bold')
                current_category = row[0]

        flowable_table.setStyle(style)
        elements.append(flowable_table)

        pdf.build(elements)
        return path
    
    '''
        Imprime o relatório de Fechamento de Caixa

        Retorna...
            Valores positivos - Sucesso;
            Valores nulos - Nenhuma comanda foi cadastrada na data selecionada.
    '''
    def make_order_report(self, selected_date):
        return db.fetch_order_report(selected_date)

    '''
        Função para carregar o tema persistido na memória
    '''
    def fetch_curr_theme(self):
        try:
            with open('data/curr_theme.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return 'litera' # retorna o tema padrão