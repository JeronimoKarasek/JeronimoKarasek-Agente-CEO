-- Supabase schema placeholder.
-- Copy full DDL from the HTML guide if desired.
create extension if not exists pgcrypto;

create table if not exists products (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  niche text,
  cost numeric(12,2),
  price numeric(12,2),
  status text default 'draft',
  created_at timestamptz not null default now()
);

create table if not exists creatives (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null,
  variant int,
  status text default 'queued',
  created_at timestamptz not null default now()
);

create table if not exists publications (
  id uuid primary key default gen_random_uuid(),
  creative_id uuid not null,
  platform text,
  status text default 'queued',
  created_at timestamptz not null default now()
);

create table if not exists campaigns (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  platform text not null,
  daily_budget numeric(12,2) default 0,
  status text default 'draft',
  created_at timestamptz not null default now()
);

create table if not exists orders (
  id uuid primary key default gen_random_uuid(),
  external_id text,
  status text,
  revenue numeric(12,2) default 0,
  created_at timestamptz not null default now()
);
