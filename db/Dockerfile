FROM postgres:15-alpine
COPY ./init.sql /docker-entrypoint-initdb.d/
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres

EXPOSE 5432