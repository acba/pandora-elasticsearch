from datetime import datetime
from elasticsearch_dsl import Document, Text, Date, Integer

class PaginaDiarioOficial(Document):
    pagina = Integer()
    base64 = Text()
    texto = Text()
    criado = Date()
    filename = Text()
    hostname = Text()

    class Index:
        name = 'diario-oficial'

    def save(self, ** kwargs):
        self.criado = datetime.now()
        return super().save(** kwargs)

class Outro(Document):
    pagina = int()
    base64 = Text()
    texto = Text()
    criado = Date()
    filename = Text()

    class Index:
        name = 'diario-oficial'

    def save(self, ** kwargs):
        self.criado = datetime.now()
        return super().save(** kwargs)
