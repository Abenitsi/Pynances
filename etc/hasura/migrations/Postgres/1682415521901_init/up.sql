SET check_function_bodies = false;
CREATE FOREIGN TABLE public.receipt_lines (
    id text,
    receipt_id text,
    amount integer,
    concept text
)
SERVER mysql_server
OPTIONS (
    dbname 'nester',
    table_name 'receipt_lines'
);
CREATE FOREIGN TABLE public.receipts (
    id text,
    serial_number text,
    description text
)
SERVER mysql_server
OPTIONS (
    dbname 'nester',
    table_name 'receipts'
);
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
