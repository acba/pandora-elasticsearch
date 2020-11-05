import requests
import base64
import pdfplumber
import io
import os
from urllib.parse import urlparse

from flask import Flask, request
from elasticsearch_dsl import connections

from model import PaginaDiarioOficial

def connect():
    """Cria conexão com o Elasticsearch """
    connections.create_connection(hosts=['localhost'], timeout=20)

def get_pdf(url):
    try:
        response = requests.get(url)
        print(f'Download realizado - {response.status_code}')

        temp = io.BytesIO()
        temp.write(response.content)
        
        return pdfplumber.open(temp)
    except:
        return None

def get_filename(url):
    return os.path.basename(url)

def get_hostname(url):
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}'

def save(pdf, url):
    filename = get_filename(url)
    hostname = get_hostname(url)
    print(f'Salvando: {filename} do dominio {hostname}')

    for page in pdf.pages:
        texto = page.extract_text()
        # print(f'Texto: {texto}')

        texto_base64 = base64.b64encode(bytes(texto, 'utf-8')).decode('utf-8')
        num_pg = page.page_number

        doc = PaginaDiarioOficial(
            pagina=num_pg,
            base64=texto_base64,
            texto=texto,
            filename=filename,
            hostname=hostname,
        )

        # print('Indexando pagina do documento')
        doc.save(pipeline='diario-oficial')
        # print("Indexado")

def main():
    connect()
    print('Conexao feita')

main()
app = Flask(__name__)

@app.route('/process-pdf', methods=['POST'])
def processa_pdf():
    print(request.form['url'])
    url = request.form['url']

    pdf = get_pdf(url)
    
    if pdf is None:
        return 'Erro no processamento do pdf'

    save(pdf, url)

    return 'Processado'


