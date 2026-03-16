CREATE DATABASE IF NOT EXISTS todo_db;

\c todo_db;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'todo_user') THEN
        CREATE USER todo_user WITH PASSWORD 'todo_password';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE todo_db TO todo_user;
GRANT ALL ON SCHEMA public TO todo_user;