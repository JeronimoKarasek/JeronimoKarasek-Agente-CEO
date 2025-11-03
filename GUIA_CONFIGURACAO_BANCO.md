# 🔧 GUIA DE CONFIGURAÇÃO DO BANCO DE DADOS SUPABASE

## ❌ Erro Encontrado
```
ERROR: 42703: column "id" does not exist
```

Este erro geralmente ocorre quando:
1. As tabelas foram criadas parcialmente
2. Há conflito com índices existentes
3. O schema anterior não foi limpo corretamente

---

## ✅ SOLUÇÃO: 3 Opções

### 📋 OPÇÃO 1: Script Seguro (RECOMENDADO)

Use o arquivo `supabase/schema_safe.sql` que:
- Remove todas as tabelas existentes
- Recria tudo do zero
- Adiciona índices e configurações

**Passo a passo:**

1. **Acesse seu Supabase Dashboard**
   - URL: https://app.supabase.com
   - Entre no seu projeto

2. **Vá para SQL Editor**
   - Clique em "SQL Editor" no menu lateral
   - Ou acesse: https://app.supabase.com/project/YOUR_PROJECT/sql

3. **Cole o script**
   - Copie todo o conteúdo de `supabase/schema_safe.sql`
   - Cole no editor SQL

4. **Execute**
   - Clique em "Run" ou pressione Ctrl+Enter
   - Aguarde a execução (~5-10 segundos)

5. **Verifique**
   - Vá em "Table Editor"
   - Confirme que todas as tabelas foram criadas

---

### 📋 OPÇÃO 2: Limpeza Manual

Se preferir limpar manualmente:

```sql
-- 1. Remover views materializadas
drop materialized view if exists mv_campaign_cac cascade;
drop materialized view if exists mv_daily_roas cascade;

-- 2. Remover todas as tabelas
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

-- 3. Agora execute o schema original
-- Use o conteúdo de supabase/schema.sql
```

---

### 📋 OPÇÃO 3: Verificação e Correção

Se só algumas tabelas têm problemas:

```sql
-- Verificar quais tabelas existem
select table_name 
from information_schema.tables 
where table_schema = 'public' 
order by table_name;

-- Ver estrutura de uma tabela específica
select column_name, data_type, column_default
from information_schema.columns
where table_name = 'products'  -- mude o nome conforme necessário
order by ordinal_position;

-- Remover tabela problemática específica
drop table if exists products cascade;

-- Recriar apenas essa tabela
create table products (
  id uuid primary key default gen_random_uuid(),
  workspace_id text not null default 'default',
  title text not null,
  -- ... resto da definição
);
```

---

## 🔍 DIAGNÓSTICO: Identificar o Problema

Execute este SQL para ver o estado atual:

```sql
-- Ver todas as tabelas
select 
  table_name,
  (select count(*) from information_schema.columns 
   where table_name = t.table_name and table_schema = 'public') as column_count
from information_schema.tables t
where table_schema = 'public' 
  and table_type = 'BASE TABLE'
order by table_name;

-- Ver índices
select tablename, indexname
from pg_indexes
where schemaname = 'public'
order by tablename, indexname;

-- Ver views materializadas
select matviewname
from pg_matviews
where schemaname = 'public';
```

---

## ✅ VALIDAÇÃO PÓS-INSTALAÇÃO

Após executar o script, valide com:

```sql
-- 1. Contar tabelas (deve retornar 14)
select count(*) as total_tables
from information_schema.tables
where table_schema = 'public' 
  and table_type = 'BASE TABLE';

-- 2. Verificar se todas as tabelas principais existem
select 
  case when exists (select 1 from information_schema.tables where table_name = 'products') then '✓' else '✗' end as products,
  case when exists (select 1 from information_schema.tables where table_name = 'creatives') then '✓' else '✗' end as creatives,
  case when exists (select 1 from information_schema.tables where table_name = 'publications') then '✓' else '✗' end as publications,
  case when exists (select 1 from information_schema.tables where table_name = 'campaigns') then '✓' else '✗' end as campaigns,
  case when exists (select 1 from information_schema.tables where table_name = 'orders') then '✓' else '✗' end as orders,
  case when exists (select 1 from information_schema.tables where table_name = 'tasks') then '✓' else '✗' end as tasks,
  case when exists (select 1 from information_schema.tables where table_name = 'config') then '✓' else '✗' end as config;

-- 3. Verificar config padrão foi inserida
select * from config where workspace_id = 'default';

-- 4. Testar inserção em uma tabela
insert into products (title, status) 
values ('Test Product', 'draft')
returning id, title, created_at;

-- 5. Se deu certo, limpar teste
delete from products where title = 'Test Product';
```

---

## 🚀 APÓS CRIAÇÃO DAS TABELAS

1. **Reinicie os containers Docker:**
   ```bash
   cd /root/JeronimoKarasek-Agente-CEO-1
   docker compose restart
   ```

2. **Verifique os logs do worker:**
   ```bash
   docker compose logs -f worker
   ```
   
   Agora deve mostrar:
   ```
   ✓ Worker started (sem erros de tabela)
   ```

3. **Teste a API novamente:**
   ```bash
   curl -X POST http://localhost:8080/api/run/scout \
     -H "Content-Type: application/json" \
     -d '{"search_term": "test product", "async_mode": false}'
   ```

---

## 🔐 PERMISSÕES (Se necessário)

Se houver problemas de permissão no Supabase:

```sql
-- Dar permissões ao usuário anon (público)
grant usage on schema public to anon, authenticated;
grant select on all tables in schema public to anon, authenticated;

-- Dar permissões completas ao usuário autenticado
grant insert, update, delete on all tables in schema public to authenticated;

-- Permitir uso de sequências
grant usage on all sequences in schema public to anon, authenticated;
```

---

## 📚 ARQUIVOS DE SCHEMA DISPONÍVEIS

1. **`supabase/schema.sql`** - Schema original com `create if not exists`
2. **`supabase/schema_safe.sql`** - ✅ Schema seguro com DROP statements (RECOMENDADO)
3. **`supabase/schema_full_from_guide.sql`** - Schema completo do guia (se existir)

---

## ❓ PROBLEMAS COMUNS

### "permission denied for schema public"
**Solução:** Execute os comandos de permissão acima

### "relation already exists"
**Solução:** Use `schema_safe.sql` que remove tudo antes

### "column does not exist" após criar tabela
**Solução:** Verifique se a tabela tem todas as colunas necessárias usando:
```sql
\d products
-- ou
select * from information_schema.columns where table_name = 'products';
```

### Worker continua com erro após criar tabelas
**Solução:** Reinicie os containers:
```bash
docker compose restart
```

---

## 🎯 RESULTADO ESPERADO

Após executar o schema com sucesso, você deve ter:

✅ 14 tabelas criadas  
✅ 2 views materializadas  
✅ ~25 índices  
✅ 1 registro na tabela config  
✅ Worker sem erros de banco  
✅ API funcionando completamente  

---

## 📞 SUPORTE

Se ainda tiver problemas:

1. Verifique a versão do PostgreSQL no Supabase (deve ser >= 12)
2. Confirme que a extensão `pgcrypto` está habilitada
3. Verifique os logs no Supabase Dashboard > Logs
4. Execute o diagnóstico SQL acima e compartilhe os resultados

---

**Criado em:** 03/11/2025  
**Versão:** 1.0  
**Status:** ✅ Testado e validado
