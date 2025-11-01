-- =============================
-- EXTENSIONS & UTILITIES
-- =============================
create extension if not exists pgcrypto; -- para gen_random_uuid()

-- Função genérica para updated_at automático
create or replace function public.set_updated_at()
returns trigger as $$
begin
  new.updated_at := now();
  return new;
end;
$$ language plpgsql;

-- =============================
-- TABELAS BÁSICAS / PERFIS (opcional)
-- =============================
-- Observação: Supabase já mantém auth.users. Se precisar perfis, use:
create table if not exists public.profiles (
  id uuid primary key default auth.uid(),
  full_name text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create trigger profiles_set_updated_at
before update on public.profiles
for each row execute function public.set_updated_at();

alter table public.profiles enable row level security;
create policy "profiles_select_own" on public.profiles
for select using (id = auth.uid());
create policy "profiles_ins_own" on public.profiles
for insert with check (id = auth.uid());
create policy "profiles_upd_own" on public.profiles
for update using (id = auth.uid());

-- =============================
-- TABELAS DE NEGÓCIO
-- =============================
-- Owner model simples: todas as tabelas têm owner_id = auth.uid()
-- (Service role bypassa RLS quando necessário)

-- PRODUCTS
create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  title text not null,
  niche text,
  cost numeric(12,2) not null default 0,
  price numeric(12,2) not null default 0,
  margin_pct numeric(6,2) generated always as (
    case when price > 0 then round(((price - cost) / price) * 100, 2) else null end
  ) stored,
  source_url text,
  media_url text,
  status text not null default 'draft' check (status in ('draft','testing','active','paused','archived')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_products_owner on public.products(owner_id);
create index if not exists idx_products_status on public.products(status);

create trigger products_set_updated_at
before update on public.products
for each row execute function public.set_updated_at();

alter table public.products enable row level security;
create policy "products_select_own" on public.products
for select using (owner_id = auth.uid());
create policy "products_ins_own" on public.products
for insert with check (owner_id = auth.uid());
create policy "products_upd_own" on public.products
for update using (owner_id = auth.uid());
create policy "products_del_own" on public.products
for delete using (owner_id = auth.uid());

-- PRODUCT SOURCES
create table if not exists public.product_sources (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  product_id uuid not null references public.products(id) on delete cascade,
  vendor text not null,
  vendor_product_id text,
  buy_url text,
  stock_hint int,
  shipping_sla text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_product_sources_product on public.product_sources(product_id);
create index if not exists idx_product_sources_owner on public.product_sources(owner_id);
create trigger product_sources_set_updated_at
before update on public.product_sources
for each row execute function public.set_updated_at();
alter table public.product_sources enable row level security;
create policy "product_sources_select_own" on public.product_sources for select using (owner_id = auth.uid());
create policy "product_sources_ins_own" on public.product_sources for insert with check (owner_id = auth.uid());
create policy "product_sources_upd_own" on public.product_sources for update using (owner_id = auth.uid());
create policy "product_sources_del_own" on public.product_sources for delete using (owner_id = auth.uid());

-- CREATIVES
create table if not exists public.creatives (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  product_id uuid not null references public.products(id) on delete cascade,
  status text not null default 'draft' check (status in ('draft','ready','queued','published','failed')),
  variant text,
  hook text,
  script text,
  cta text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_creatives_product on public.creatives(product_id);
create index if not exists idx_creatives_owner on public.creatives(owner_id);
create trigger creatives_set_updated_at
before update on public.creatives
for each row execute function public.set_updated_at();
alter table public.creatives enable row level security;
create policy "creatives_select_own" on public.creatives for select using (owner_id = auth.uid());
create policy "creatives_ins_own" on public.creatives for insert with check (owner_id = auth.uid());
create policy "creatives_upd_own" on public.creatives for update using (owner_id = auth.uid());
create policy "creatives_del_own" on public.creatives for delete using (owner_id = auth.uid());

-- CREATIVE ASSETS
create table if not exists public.creative_assets (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  creative_id uuid not null references public.creatives(id) on delete cascade,
  asset_type text not null check (asset_type in ('thumbnail','video','caption')),
  storage_path text not null,
  duration_seconds int,
  checksum text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_creative_assets_creative on public.creative_assets(creative_id);
create index if not exists idx_creative_assets_owner on public.creative_assets(owner_id);
create trigger creative_assets_set_updated_at
before update on public.creative_assets
for each row execute function public.set_updated_at();
alter table public.creative_assets enable row level security;
create policy "creative_assets_select_own" on public.creative_assets for select using (owner_id = auth.uid());
create policy "creative_assets_ins_own" on public.creative_assets for insert with check (owner_id = auth.uid());
create policy "creative_assets_upd_own" on public.creative_assets for update using (owner_id = auth.uid());
create policy "creative_assets_del_own" on public.creative_assets for delete using (owner_id = auth.uid());

-- PUBLICATIONS
create table if not exists public.publications (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  creative_id uuid not null references public.creatives(id) on delete cascade,
  platform text not null check (platform in ('tiktok','instagram','youtube')),
  scheduled_at timestamptz,
  published_at timestamptz,
  post_url text,
  status text not null default 'queued' check (status in ('queued','published','failed')),
  error text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_publications_creative on public.publications(creative_id);
create index if not exists idx_publications_owner on public.publications(owner_id);
create trigger publications_set_updated_at
before update on public.publications
for each row execute function public.set_updated_at();
alter table public.publications enable row level security;
create policy "publications_select_own" on public.publications for select using (owner_id = auth.uid());
create policy "publications_ins_own" on public.publications for insert with check (owner_id = auth.uid());
create policy "publications_upd_own" on public.publications for update using (owner_id = auth.uid());
create policy "publications_del_own" on public.publications for delete using (owner_id = auth.uid());

-- AD ACCOUNTS & PIXELS
create table if not exists public.ad_accounts (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  platform text not null check (platform in ('meta','tiktok')),
  external_id text not null,
  name text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_ad_accounts_owner on public.ad_accounts(owner_id);
create trigger ad_accounts_set_updated_at
before update on public.ad_accounts
for each row execute function public.set_updated_at();
alter table public.ad_accounts enable row level security;
create policy "ad_accounts_select_own" on public.ad_accounts for select using (owner_id = auth.uid());
create policy "ad_accounts_ins_own" on public.ad_accounts for insert with check (owner_id = auth.uid());
create policy "ad_accounts_upd_own" on public.ad_accounts for update using (owner_id = auth.uid());
create policy "ad_accounts_del_own" on public.ad_accounts for delete using (owner_id = auth.uid());

create table if not exists public.pixels (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  platform text not null check (platform in ('meta','tiktok')),
  ad_account_id uuid not null references public.ad_accounts(id) on delete cascade,
  external_id text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_pixels_owner on public.pixels(owner_id);
create index if not exists idx_pixels_account on public.pixels(ad_account_id);
create trigger pixels_set_updated_at
before update on public.pixels
for each row execute function public.set_updated_at();
alter table public.pixels enable row level security;
create policy "pixels_select_own" on public.pixels for select using (owner_id = auth.uid());
create policy "pixels_ins_own" on public.pixels for insert with check (owner_id = auth.uid());
create policy "pixels_upd_own" on public.pixels for update using (owner_id = auth.uid());
create policy "pixels_del_own" on public.pixels for delete using (owner_id = auth.uid());

-- CAMPAIGNS / ADSETS / ADS / TRAFFIC METRICS
create table if not exists public.campaigns (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  platform text not null check (platform in ('meta','tiktok')),
  ad_account_id uuid not null references public.ad_accounts(id) on delete cascade,
  name text not null,
  objective text,
  status text not null default 'draft' check (status in ('draft','active','paused','deleted')),
  daily_budget numeric(12,2) default 0,
  spend numeric(12,2) default 0,
  clicks int default 0,
  impressions int default 0,
  purchases int default 0,
  roas numeric(8,2),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_campaigns_owner on public.campaigns(owner_id);
create index if not exists idx_campaigns_account on public.campaigns(ad_account_id);
create trigger campaigns_set_updated_at
before update on public.campaigns
for each row execute function public.set_updated_at();
alter table public.campaigns enable row level security;
create policy "campaigns_select_own" on public.campaigns for select using (owner_id = auth.uid());
create policy "campaigns_ins_own" on public.campaigns for insert with check (owner_id = auth.uid());
create policy "campaigns_upd_own" on public.campaigns for update using (owner_id = auth.uid());
create policy "campaigns_del_own" on public.campaigns for delete using (owner_id = auth.uid());

create table if not exists public.adsets (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  campaign_id uuid not null references public.campaigns(id) on delete cascade,
  name text not null,
  targeting_json jsonb,
  bid_strategy text,
  status text not null default 'draft' check (status in ('draft','active','paused','deleted')),
  budget numeric(12,2) default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_adsets_campaign on public.adsets(campaign_id);
create index if not exists idx_adsets_owner on public.adsets(owner_id);
create trigger adsets_set_updated_at
before update on public.adsets
for each row execute function public.set_updated_at();
alter table public.adsets enable row level security;
create policy "adsets_select_own" on public.adsets for select using (owner_id = auth.uid());
create policy "adsets_ins_own" on public.adsets for insert with check (owner_id = auth.uid());
create policy "adsets_upd_own" on public.adsets for update using (owner_id = auth.uid());
create policy "adsets_del_own" on public.adsets for delete using (owner_id = auth.uid());

create table if not exists public.ads (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  adset_id uuid not null references public.adsets(id) on delete cascade,
  name text not null,
  creative_ref text,
  status text not null default 'draft' check (status in ('draft','active','paused','deleted')),
  cpc numeric(10,4),
  cpm numeric(10,4),
  ctr numeric(6,4),
  spend numeric(12,2) default 0,
  purchases int default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_ads_adset on public.ads(adset_id);
create index if not exists idx_ads_owner on public.ads(owner_id);
create trigger ads_set_updated_at
before update on public.ads
for each row execute function public.set_updated_at();
alter table public.ads enable row level security;
create policy "ads_select_own" on public.ads for select using (owner_id = auth.uid());
create policy "ads_ins_own" on public.ads for insert with check (owner_id = auth.uid());
create policy "ads_upd_own" on public.ads for update using (owner_id = auth.uid());
create policy "ads_del_own" on public.ads for delete using (owner_id = auth.uid());

create table if not exists public.traffic_metrics (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  date date not null,
  level text not null check (level in ('campaign','adset','ad')),
  ref_id uuid not null,
  spend numeric(12,2) default 0,
  clicks int default 0,
  impressions int default 0,
  purchases int default 0,
  revenue numeric(12,2),
  roas numeric(8,2),
  cac numeric(12,2),
  created_at timestamptz not null default now()
);
create index if not exists idx_traffic_metrics_owner_date on public.traffic_metrics(owner_id, date);
create index if not exists idx_traffic_metrics_ref on public.traffic_metrics(ref_id);
alter table public.traffic_metrics enable row level security;
create policy "traffic_metrics_select_own" on public.traffic_metrics for select using (owner_id = auth.uid());
create policy "traffic_metrics_ins_own" on public.traffic_metrics for insert with check (owner_id = auth.uid());

-- CLIENTES / LEADS / ORDERS
create table if not exists public.customers (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  name text,
  email text,
  phone text,
  first_seen_at timestamptz default now(),
  last_seen_at timestamptz,
  ltv numeric(12,2) default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_customers_owner on public.customers(owner_id);
create index if not exists idx_customers_email on public.customers(email);
create trigger customers_set_updated_at
before update on public.customers
for each row execute function public.set_updated_at();
alter table public.customers enable row level security;
create policy "customers_select_own" on public.customers for select using (owner_id = auth.uid());
create policy "customers_ins_own" on public.customers for insert with check (owner_id = auth.uid());
create policy "customers_upd_own" on public.customers for update using (owner_id = auth.uid());
create policy "customers_del_own" on public.customers for delete using (owner_id = auth.uid());

create table if not exists public.leads (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  source text,
  product_id uuid references public.products(id) on delete set null,
  customer_id uuid references public.customers(id) on delete set null,
  utm_json jsonb,
  stage text default 'new' check (stage in ('new','contacted','qualified','won','lost')),
  created_at timestamptz not null default now()
);
create index if not exists idx_leads_owner on public.leads(owner_id);
create index if not exists idx_leads_customer on public.leads(customer_id);
alter table public.leads enable row level security;
create policy "leads_select_own" on public.leads for select using (owner_id = auth.uid());
create policy "leads_ins_own" on public.leads for insert with check (owner_id = auth.uid());
create policy "leads_upd_own" on public.leads for update using (owner_id = auth.uid());
create policy "leads_del_own" on public.leads for delete using (owner_id = auth.uid());

create table if not exists public.orders (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  customer_id uuid references public.customers(id) on delete set null,
  product_id uuid references public.products(id) on delete set null,
  quantity int not null default 1,
  price numeric(12,2) not null default 0,
  discount numeric(12,2) default 0,
  revenue numeric(12,2) generated always as (round((price - coalesce(discount,0)) * quantity, 2)) stored,
  cost_product numeric(12,2) default 0,
  cost_shipping numeric(12,2) default 0,
  fees numeric(12,2) default 0,
  channel text,
  utm_json jsonb,
  campaign_ref uuid,
  purchased_at timestamptz not null default now(),
  status text default 'paid' check (status in ('paid','refunded','canceled','pending')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists idx_orders_owner on public.orders(owner_id);
create index if not exists idx_orders_customer on public.orders(customer_id);
create index if not exists idx_orders_product on public.orders(product_id);
create trigger orders_set_updated_at
before update on public.orders
for each row execute function public.set_updated_at();
alter table public.orders enable row level security;
create policy "orders_select_own" on public.orders for select using (owner_id = auth.uid());
create policy "orders_ins_own" on public.orders for insert with check (owner_id = auth.uid());
create policy "orders_upd_own" on public.orders for update using (owner_id = auth.uid());
create policy "orders_del_own" on public.orders for delete using (owner_id = auth.uid());

create table if not exists public.order_items (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  order_id uuid not null references public.orders(id) on delete cascade,
  sku text,
  qty int not null default 1,
  unit_price numeric(12,2) not null default 0
);
create index if not exists idx_order_items_order on public.order_items(order_id);
create index if not exists idx_order_items_owner on public.order_items(owner_id);
alter table public.order_items enable row level security;
create policy "order_items_select_own" on public.order_items for select using (owner_id = auth.uid());
create policy "order_items_ins_own" on public.order_items for insert with check (owner_id = auth.uid());
create policy "order_items_upd_own" on public.order_items for update using (owner_id = auth.uid());
create policy "order_items_del_own" on public.order_items for delete using (owner_id = auth.uid());

-- ALERTS / TASKS / AUDIT
create table if not exists public.alerts (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  severity text not null check (severity in ('INFO','LOW','MEDIUM','HIGH','CRITICAL')),
  title text not null,
  message text,
  ref_table text,
  ref_id uuid,
  ack boolean default false,
  created_at timestamptz not null default now()
);
create index if not exists idx_alerts_owner on public.alerts(owner_id);
alter table public.alerts enable row level security;
create policy "alerts_select_own" on public.alerts for select using (owner_id = auth.uid());
create policy "alerts_ins_own" on public.alerts for insert with check (owner_id = auth.uid());

create table if not exists public.tasks (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  agent text not null,
  action text not null,
  payload_json jsonb,
  status text not null default 'pending' check (status in ('pending','running','done','failed')),
  result_json jsonb,
  started_at timestamptz,
  finished_at timestamptz,
  created_at timestamptz not null default now()
);
create index if not exists idx_tasks_owner on public.tasks(owner_id);
create index if not exists idx_tasks_status on public.tasks(status);
alter table public.tasks enable row level security;
create policy "tasks_select_own" on public.tasks for select using (owner_id = auth.uid());
create policy "tasks_ins_own" on public.tasks for insert with check (owner_id = auth.uid());
create policy "tasks_upd_own" on public.tasks for update using (owner_id = auth.uid());

create table if not exists public.audit_log (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid(),
  actor text not null,
  action text not null,
  details_json jsonb,
  created_at timestamptz not null default now()
);
create index if not exists idx_audit_owner on public.audit_log(owner_id);
alter table public.audit_log enable row level security;
create policy "audit_select_own" on public.audit_log for select using (owner_id = auth.uid());
create policy "audit_ins_own" on public.audit_log for insert with check (owner_id = auth.uid());

-- =============================
-- VIEWS ÚTEIS (SUMÁRIO DE MÉTRICAS)
-- =============================
create or replace view public.metrics_daily as
select
  o.owner_id,
  date_trunc('day', o.purchased_at) as day,
  count(*) as orders,
  sum(o.revenue) as revenue,
  sum(o.cost_product + o.cost_shipping + o.fees) as total_cost,
  coalesce(sum(tm.spend),0) as ad_spend,
  case when coalesce(sum(tm.spend),0) > 0 then round(sum(o.revenue)/sum(tm.spend),2) else null end as roas
from public.orders o
left join public.traffic_metrics tm
  on tm.owner_id = o.owner_id
 and tm.date = date_trunc('day', o.purchased_at)::date
where o.status = 'paid'
group by 1,2
order by 2 desc;

-- =============================
-- STORAGE BUCKET (mídias)
-- =============================
-- Executar no SQL Editor; requer permissão de storage_admin
select storage.create_bucket('media', true);
