ARG ELK_VERSION

# https://github.com/elastic/logstash-docker
FROM docker.elastic.co/logstash/logstash-oss:${ELK_VERSION}

COPY postgresql-42.2.5.jar /opt/
# Add your logstash plugins setup here
RUN logstash-plugin install logstash-input-jdbc
