-- Create schema tables (minimal dev schema)
\i supabase/schema.sql

-- Track migration
create table if not exists schema_migrations (version text primary key, applied_at timestamptz not null default now());
insert into schema_migrations(version) values ('0001_base') on conflict do nothing;

