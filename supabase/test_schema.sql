-- Quick Test Script - Execute este SQL para testar se tudo está OK

-- 1. Verificar extensões
select extname from pg_extension where extname = 'pgcrypto';
-- Esperado: pgcrypto

-- 2. Contar tabelas
select count(*) as total_tables
from information_schema.tables
where table_schema = 'public' and table_type = 'BASE TABLE';
-- Esperado: 14

-- 3. Listar todas as tabelas
select table_name 
from information_schema.tables 
where table_schema = 'public' and table_type = 'BASE TABLE'
order by table_name;

-- 4. Verificar estrutura da tabela products
select column_name, data_type, column_default, is_nullable
from information_schema.columns
where table_name = 'products'
order by ordinal_position;

-- 5. Verificar config default
select * from config where workspace_id = 'default';

-- 6. Teste de inserção
begin;
  insert into products (title, status) values ('Test Product', 'draft') returning *;
rollback;

-- Se todos os testes passarem, está tudo OK! ✅
