import json
import base64
import pdfplumber
from elasticsearch_dsl import connections

from model import PaginaDiarioOficial


def connect():
    """Cria conexão com o Elasticsearch """
    connections.create_connection(hosts=['localhost'], timeout=20)

def main():
    connect()

    # with pdfplumber.open('../dados/2019-06-07-DiarioOficialMPPB.pdf') as pdf:
    with pdfplumber.open('../dados/edital_de_abertura_n_001_2020.pdf') as pdf:
        # first_page = pdf.pages[0]
        # print(first_page.extract_text())
        # print(first_page.chars[0])

        dado = {}
        dado['meta'] = pdf.metadata
        dado['dados'] = []

        for page in pdf.pages:
            texto = page.extract_text()
            texto_base64 = base64.b64encode(bytes(texto, 'utf-8')).decode('utf-8')
            num_pg = page.page_number

            doc = PaginaDiarioOficial(
                pagina=num_pg,
                base64=texto_base64,
                texto=texto,
            )

            print('Indexando pagina do documento')
            doc.save(pipeline='diario-oficial')
            print("Indexado")

        

main()