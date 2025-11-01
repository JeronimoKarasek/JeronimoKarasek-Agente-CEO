This folder holds SQL migrations for the Supabase Postgres database.

Suggested workflow:
- Track applied versions in a `schema_migrations` table (version TEXT PRIMARY KEY, applied_at TIMESTAMPTZ DEFAULT now()).
- Apply each `NNNN_name.sql` in order; record version in `schema_migrations`.
- For Supabase, paste SQL in the SQL Editor or run via `psql` if available.

