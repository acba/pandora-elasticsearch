FROM elasticsearch:7.9.3

RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install --batch ingest-attachment
