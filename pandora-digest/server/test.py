import requests
import base64
import urllib3
import pdfplumber
import io

from elasticsearch_dsl import connections

connections.create_connection(hosts=['localhost'], timeout=20)

url = 'https://arquivo.pciconcursos.com.br/cro-pe-anuncia-novo-concurso-publico-para-niveis-medio-e-superior/1517503/57605b9807/edital_de_abertura_n_001_2020.pdf'

response = requests.get(url)
print('Download realizado')
print(response.status_code)

http = urllib3.PoolManager()
temp = io.BytesIO()
temp.write(http.request("GET", url).data)

with pdfplumber.open(response.content) as pdf:
    for page in pdf.pages:
        texto = page.extract_text()
        texto_base64 = base64.b64encode(bytes(texto, 'utf-8')).decode('utf-8')
        num_pg = page.page_number

        print(f'Texto: {texto}')
        print(f'Indexando pagina {num_pg} do documento')


# def save(stream):
#     with pdfplumber.open(stream) as pdf:
#         for page in pdf.pages:
#             texto = page.extract_text()
#             texto_base64 = base64.b64encode(bytes(texto, 'utf-8')).decode('utf-8')
#             num_pg = page.page_number

#             doc = PaginaDiarioOficial(
#                 pagina=num_pg,
#                 base64=texto_base64,
#                 texto=texto,
#             )

#             print('Indexando pagina do documento')
#             doc.save(pipeline='diario-oficial')
#             print("Indexado")

# def main():
#     connect()
#     print('Conexao feita')

# main()

# app = Flask(__name__)

# @app.route('/process-pdf', methods=['POST'])
# def processa_pdf():
#     print(request.form['url'])
#     url = request.form['url']

    
#     save(response.content)

#     return 'Processado'


