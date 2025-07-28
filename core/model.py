from core.components.SGBD import *
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime

class Model:
    def __init__(self):
        self.__item = {
            'name': '',
            'cost': 0.0,
            'price': 0.0,
            'qty': 0
        }

        self.__stock = []

    # imprime o relatório do estoque em arquivo PDF
    #
    # retorna...
    # 0 - sucesso
    # 1 - estoque vazio
    def make_stock_report(self):
        table = [
            ['Produto', 'Custo', 'Preço', 'Quantidade']
        ]

        self.__stock = fetch_stock()

        if self.__stock == []:
            return 1

        for item in self.__stock:
            row = []

            row.append(item['name'])
            row.append(item['cost'])
            row.append(item['price'])
            row.append(item['qty'])

            table.append(row)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # persiste o arquivo CSV
        with open('data/stock ' + timestamp + '.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(table)

        # cria o documento PDF
        pdf = SimpleDocTemplate('data/stock ' + timestamp + '.pdf', pagesize=A4, title='Relatório do Estoque: ' + timestamp)
        elements = []

        # converte a lista para um flowable Table do ReportLab
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