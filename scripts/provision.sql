DROP DATABASE IF EXISTS studentdb;

DROP USER IF EXISTS student;

CREATE USER student WITH PASSWORD 'student';

ALTER USER student WITH CREATEDB;

CREATE DATABASE studentdb WITH OWNER student;
