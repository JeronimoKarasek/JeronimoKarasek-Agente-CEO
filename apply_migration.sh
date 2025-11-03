#!/bin/bash
# Script para aplicar migration de credenciais no Supabase
# Execute este script depois de configurar suas credenciais Supabase

echo "🔧 Aplicando Migration 0002_config_credentials..."
echo ""
echo "⚠️  Você precisa executar este SQL no Supabase SQL Editor:"
echo "    https://supabase.com/dashboard/project/_/sql"
echo ""
echo "📋 Cole este SQL no editor:"
echo "============================================================"
cat << 'EOF'

-- Migration: Add credential columns to config table
ALTER TABLE config ADD COLUMN IF NOT EXISTS supabase_url TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS supabase_anon_key TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS supabase_service_key TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_access_token TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_ad_account_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_pixel_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_app_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_app_secret TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS instagram_business_account_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS tiktok_access_token TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS tiktok_advertiser_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS tiktok_open_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS tiktok_pixel_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS daily_budget_cap NUMERIC(10, 2) DEFAULT 300.0;
ALTER TABLE config ADD COLUMN IF NOT EXISTS weekly_budget_cap NUMERIC(10, 2) DEFAULT 1500.0;
ALTER TABLE config ADD COLUMN IF NOT EXISTS storage_bucket TEXT DEFAULT 'media';
ALTER TABLE config ADD COLUMN IF NOT EXISTS proxy_server TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS proxy_username TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS proxy_password TEXT;

CREATE INDEX IF NOT EXISTS idx_config_workspace ON config(workspace_id);

COMMENT ON COLUMN config.supabase_service_key IS 'Sensitive: Service role key';
COMMENT ON COLUMN config.meta_access_token IS 'Sensitive: Meta API token';
COMMENT ON COLUMN config.meta_app_secret IS 'Sensitive: Meta app secret';
COMMENT ON COLUMN config.tiktok_access_token IS 'Sensitive: TikTok API token';
COMMENT ON COLUMN config.proxy_password IS 'Sensitive: Proxy password';

EOF
echo "============================================================"
echo ""
echo "✅ Depois de executar, pressione Enter para continuar..."
read

echo "🧪 Testando conexão com API..."
curl -s http://103.199.187.127:8080/api/admin/config | jq .

echo ""
echo "✅ Migration concluída!"
echo "📱 Acesse: http://mkt.farolbase.com/index_complete.html"
echo "⚙️  Vá na aba Configuração e adicione suas credenciais"
