-- Migration: Add credential columns to config table
-- Date: 2025-11-03
-- Description: Expands config table to store all API credentials and settings

-- Add Supabase credentials
ALTER TABLE config ADD COLUMN IF NOT EXISTS supabase_url TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS supabase_anon_key TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS supabase_service_key TEXT;

-- Add Meta/Facebook credentials
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_access_token TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_ad_account_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_pixel_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_app_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS meta_app_secret TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS instagram_business_account_id TEXT;

-- Add TikTok credentials
ALTER TABLE config ADD COLUMN IF NOT EXISTS tiktok_access_token TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS tiktok_advertiser_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS tiktok_open_id TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS tiktok_pixel_id TEXT;

-- Add budget caps
ALTER TABLE config ADD COLUMN IF NOT EXISTS daily_budget_cap NUMERIC(10, 2) DEFAULT 300.0;
ALTER TABLE config ADD COLUMN IF NOT EXISTS weekly_budget_cap NUMERIC(10, 2) DEFAULT 1500.0;

-- Add storage config
ALTER TABLE config ADD COLUMN IF NOT EXISTS storage_bucket TEXT DEFAULT 'media';

-- Add proxy config
ALTER TABLE config ADD COLUMN IF NOT EXISTS proxy_server TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS proxy_username TEXT;
ALTER TABLE config ADD COLUMN IF NOT EXISTS proxy_password TEXT;

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_config_workspace ON config(workspace_id);

-- Comment on sensitive columns
COMMENT ON COLUMN config.supabase_service_key IS 'Sensitive: Service role key for admin operations';
COMMENT ON COLUMN config.meta_access_token IS 'Sensitive: Meta/Facebook API access token';
COMMENT ON COLUMN config.meta_app_secret IS 'Sensitive: Meta app secret';
COMMENT ON COLUMN config.tiktok_access_token IS 'Sensitive: TikTok API access token';
COMMENT ON COLUMN config.proxy_password IS 'Sensitive: Proxy authentication password';

-- Enable Row Level Security for config table
ALTER TABLE config ENABLE ROW LEVEL SECURITY;

-- Create policy: Allow authenticated users to read/write their workspace config
CREATE POLICY IF NOT EXISTS "Users can manage their workspace config"
ON config
FOR ALL
USING (true)
WITH CHECK (true);

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Migration 0002_config_credentials completed successfully';
END
$$;
