-- Delete existing config
DROP USER MAPPING IF EXISTS FOR postgres SERVER mysql_server ;
DROP SERVER IF EXISTS mysql_server;
DROP EXTENSION IF EXISTS mysql_fdw;

-- load extension first time after install
CREATE EXTENSION mysql_fdw;

-- create server object
CREATE SERVER mysql_server
	FOREIGN DATA WRAPPER mysql_fdw
	OPTIONS (host 'mysql', port '3306');

-- create user mapping
CREATE USER MAPPING FOR postgres
	SERVER mysql_server
	OPTIONS (username 'nester', password 'nester');
