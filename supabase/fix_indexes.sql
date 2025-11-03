-- Fix para o erro de ON CONFLICT
-- Execute este SQL no Supabase para corrigir os índices únicos

-- Remover índices parciais problemáticos
drop index if exists ux_products_idem;
drop index if exists ux_creatives_idem;
drop index if exists ux_publications_idem;
drop index if exists ux_campaigns_idem;
drop index if exists ux_tasks_idem;

-- Recriar índices únicos simples (sem WHERE clause)
create unique index ux_products_idem on products(idempotency_key);
create unique index ux_creatives_idem on creatives(idempotency_key);
create unique index ux_publications_idem on publications(idempotency_key);
create unique index ux_campaigns_idem on campaigns(idempotency_key);
create unique index ux_tasks_idem on tasks(idempotency_key);

-- Alternativamente, se quiser manter a constraint parcial, use isto:
-- drop index if exists ux_products_idem;
-- alter table products add constraint ux_products_idem unique (workspace_id, idempotency_key);
