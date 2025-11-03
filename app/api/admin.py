from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.queue import TaskQueue
from ..core.db import get_client
from ..services.config import get_flags

router = APIRouter(prefix="/api/admin")
queue = TaskQueue()


class ConfigUpdate(BaseModel):
    workspace_id: str = "default"
    
    # Supabase
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_key: str | None = None
    
    # Meta/Facebook
    meta_access_token: str | None = None
    meta_ad_account_id: str | None = None
    meta_pixel_id: str | None = None
    meta_app_id: str | None = None
    meta_app_secret: str | None = None
    instagram_business_account_id: str | None = None
    
    # TikTok
    tiktok_access_token: str | None = None
    tiktok_advertiser_id: str | None = None
    tiktok_open_id: str | None = None
    tiktok_pixel_id: str | None = None
    
    # Application Settings
    auto_mode: bool | None = None
    approval_mode: bool | None = None
    dry_run: bool | None = None
    target_roas: float | None = None
    daily_budget_cap: float | None = None
    weekly_budget_cap: float | None = None
    
    # Storage
    storage_bucket: str | None = None
    
    # Proxy
    proxy_server: str | None = None
    proxy_username: str | None = None
    proxy_password: str | None = None


@router.get("/queue")
async def get_queue():
    return {"queued": queue.count_queued()}


@router.get("/alerts")
async def get_alerts(workspace_id: str = "default"):
    res = get_client().table("alerts").select("*").eq("workspace_id", workspace_id).order("created_at", desc=True).limit(50).execute()
    return res.data or []


@router.get("/audit")
async def get_audit(workspace_id: str = "default"):
    res = get_client().table("audit_log").select("*").eq("workspace_id", workspace_id).order("created_at", desc=True).limit(100).execute()
    return res.data or []


@router.get("/config")
async def read_config(workspace_id: str = "default"):
    """Retorna todas as configurações (credenciais sensíveis são mascaradas)"""
    try:
        # Busca do banco
        res = get_client().table("config").select("*").eq("workspace_id", workspace_id).execute()
        
        if res.data and len(res.data) > 0:
            config = res.data[0]
            
            # Mascara credenciais sensíveis
            sensitive_fields = [
                'supabase_anon_key', 'supabase_service_key',
                'meta_access_token', 'meta_app_secret',
                'tiktok_access_token', 'proxy_password'
            ]
            
            for field in sensitive_fields:
                if field in config and config[field]:
                    config[field] = '****' + config[field][-4:] if len(config[field]) > 4 else '****'
            
            return config
        else:
            # Retorna configuração padrão
            return {
                "workspace_id": workspace_id,
                "auto_mode": True,
                "approval_mode": False,
                "dry_run": False,
                "target_roas": 1.5,
                "daily_budget_cap": 300.0,
                "weekly_budget_cap": 1500.0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/config")
async def write_config(config: ConfigUpdate):
    """Salva configurações completas no banco de dados"""
    try:
        # Prepara dados para salvar
        values = {"workspace_id": config.workspace_id}
        
        # Adiciona apenas campos não-nulos
        field_mapping = {
            'supabase_url': config.supabase_url,
            'supabase_anon_key': config.supabase_anon_key,
            'supabase_service_key': config.supabase_service_key,
            'meta_access_token': config.meta_access_token,
            'meta_ad_account_id': config.meta_ad_account_id,
            'meta_pixel_id': config.meta_pixel_id,
            'meta_app_id': config.meta_app_id,
            'meta_app_secret': config.meta_app_secret,
            'instagram_business_account_id': config.instagram_business_account_id,
            'tiktok_access_token': config.tiktok_access_token,
            'tiktok_advertiser_id': config.tiktok_advertiser_id,
            'tiktok_open_id': config.tiktok_open_id,
            'tiktok_pixel_id': config.tiktok_pixel_id,
            'auto_mode': config.auto_mode,
            'approval_mode': config.approval_mode,
            'dry_run': config.dry_run,
            'target_roas': config.target_roas,
            'daily_budget_cap': config.daily_budget_cap,
            'weekly_budget_cap': config.weekly_budget_cap,
            'storage_bucket': config.storage_bucket,
            'proxy_server': config.proxy_server,
            'proxy_username': config.proxy_username,
            'proxy_password': config.proxy_password,
        }
        
        for key, value in field_mapping.items():
            if value is not None:
                values[key] = value
        
        if len(values) == 1:  # Apenas workspace_id
            return {"ok": True, "message": "Nenhuma configuração para salvar"}
        
        # Salva no banco (upsert)
        get_client().table("config").upsert(values).execute()
        
        # Log de auditoria
        get_client().table("audit_log").insert({
            "workspace_id": config.workspace_id,
            "action": "config_update",
            "details": f"Configurações atualizadas: {', '.join([k for k, v in field_mapping.items() if v is not None])}"
        }).execute()
        
        return {"ok": True, "message": "Configurações salvas com sucesso"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar configurações: {str(e)}")
