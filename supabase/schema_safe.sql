-- Safe schema creation script with DROP statements
-- This script will recreate all tables from scratch

-- Enable required extensions
create extension if not exists pgcrypto;

-- Drop existing objects (in reverse dependency order)
drop materialized view if exists mv_campaign_cac cascade;
drop materialized view if exists mv_daily_roas cascade;

drop table if exists traffic_metrics cascade;
drop table if exists api_calls cascade;
drop table if exists config cascade;
drop table if exists audit_log cascade;
drop table if exists alerts cascade;
drop table if exists webhook_events cascade;
drop table if exists tasks cascade;
drop table if exists orders cascade;
drop table if exists campaigns cascade;
drop table if exists publications cascade;
drop table if exists creatives cascade;
drop table if exists products cascade;

-- Create tables
create table products (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null default 'default',
  title text not null,
  niche text,
  cost numeric(12,2),
  price numeric(12,2),
  status text default 'draft',
  idempotency_key text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index idx_products_status on products(status);
create index idx_products_updated on products(updated_at);
create unique index ux_products_idem on products(workspace_id, idempotency_key) where idempotency_key is not null;

create table creatives (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null default 'default',
  product_id uuid not null,
  variant int,
  status text default 'queued',
  preflight_score numeric(4,2),
  idempotency_key text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index idx_creatives_status on creatives(status);
create index idx_creatives_updated on creatives(updated_at);
create unique index ux_creatives_idem on creatives(workspace_id, idempotency_key) where idempotency_key is not null;

create table publications (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null default 'default',
  creative_id uuid not null,
  platform text,
  status text default 'queued',
  idempotency_key text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index idx_publications_status on publications(status);
create index idx_publications_updated on publications(updated_at);
create unique index ux_publications_idem on publications(workspace_id, idempotency_key) where idempotency_key is not null;

create table campaigns (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null default 'default',
  name text not null,
  platform text not null,
  external_id text,
  daily_budget numeric(12,2) default 0,
  status text default 'draft',
  idempotency_key text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index idx_campaigns_status on campaigns(status);
create index idx_campaigns_updated on campaigns(updated_at);
create unique index ux_campaigns_idem on campaigns(workspace_id, idempotency_key) where idempotency_key is not null;

create table orders (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null default 'default',
  external_id text,
  status text,
  revenue numeric(12,2) default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Tasks table for DB-backed queue
create table tasks (
  id uuid primary key default gen_random_uuid(),
  type text not null,
  payload jsonb not null,
  workspace_id text not null,
  status text not null default 'queued',
  attempts int not null default 0,
  max_attempts int not null default 5,
  idempotency_key text,
  scheduled_for timestamptz not null default now(),
  result_json jsonb,
  error text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index idx_tasks_status on tasks(status);
create index idx_tasks_scheduled on tasks(scheduled_for);
create unique index ux_tasks_idem on tasks(idempotency_key) where idempotency_key is not null;

-- Webhook events for replay detection
create table webhook_events (
  event_id text primary key,
  received_at bigint
);

-- Alerts and audit log (simplified)
create table alerts (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null,
  severity text not null default 'info',
  code text not null,
  message text,
  created_at timestamptz not null default now()
);

create table audit_log (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null,
  actor text not null default 'agent_ceo',
  action text not null,
  context jsonb,
  created_at timestamptz not null default now()
);

-- Feature flags / config
create table config (
  workspace_id text primary key,
  auto_mode boolean default true,
  approval_mode boolean default false,
  dry_run boolean default false,
  target_roas numeric(6,2) default 1.5,
  daily_budget_cap numeric(12,2),
  weekly_budget_cap numeric(12,2)
);

-- API calls metrics
create table api_calls (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null,
  provider text not null,
  endpoint text not null,
  status_code int,
  retries int default 0,
  api_cost_ms int,
  created_at timestamptz not null default now()
);

-- Simplified traffic metrics (partitioning can be added on Supabase directly)
create table traffic_metrics (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null default 'default',
  campaign_id uuid,
  date date not null,
  spend numeric(12,2) default 0,
  clicks int default 0,
  purchases int default 0,
  revenue numeric(12,2) default 0
);

-- Materialized views
create materialized view mv_daily_roas as
select date, workspace_id,
  case when sum(spend) > 0 then round(sum(revenue)/sum(spend),2) else null end as roas
from traffic_metrics group by date, workspace_id;

create materialized view mv_campaign_cac as
select workspace_id, campaign_id,
  case when sum(purchases) > 0 then round(sum(spend)/sum(purchases),2) else null end as cac
from traffic_metrics group by workspace_id, campaign_id;

-- Insert default config
insert into config (workspace_id, auto_mode, approval_mode, dry_run, target_roas)
values ('default', true, false, false, 1.5)
on conflict (workspace_id) do nothing;

-- Create indexes for better performance
create index idx_orders_workspace on orders(workspace_id);
create index idx_campaigns_workspace on campaigns(workspace_id);
create index idx_traffic_metrics_date on traffic_metrics(date);
create index idx_traffic_metrics_campaign on traffic_metrics(campaign_id);
create index idx_audit_log_workspace on audit_log(workspace_id);
create index idx_alerts_workspace on alerts(workspace_id);

-- Grant permissions (adjust as needed for your Supabase setup)
-- Note: Uncomment and adjust these based on your Supabase roles
-- grant usage on schema public to anon, authenticated;
-- grant select on all tables in schema public to anon, authenticated;
-- grant insert, update, delete on all tables in schema public to authenticated;

-- Success message
do $$
begin
  raise notice 'Schema created successfully!';
end $$;
