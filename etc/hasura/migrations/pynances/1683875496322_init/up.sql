SET check_function_bodies = false;
CREATE TABLE public.accounts (
    id uuid NOT NULL,
    name text NOT NULL,
    iban text NOT NULL,
    hash text NOT NULL,
    amount numeric NOT NULL
);
ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_hash_key UNIQUE (hash);
ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);
