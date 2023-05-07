CREATE FOREIGN TABLE public.users (
    id text,
    name text,
    email text
)
SERVER mysql_server
OPTIONS (
    dbname 'nester',
    table_name 'nip_users'
);
