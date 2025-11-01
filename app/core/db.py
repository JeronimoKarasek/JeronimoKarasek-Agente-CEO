from typing import Optional
from supabase import create_client, Client
from .config import settings
from loguru import logger

_supabase: Optional[Client] = None
_service_client: Optional[Client] = None


def get_client() -> Client:
    global _supabase
    if _supabase is not None:
        return _supabase
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise RuntimeError("Missing SUPABASE_URL/SUPABASE_ANON_KEY. Create .env from .env.example and fill your Supabase credentials.")
    _supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    return _supabase


def get_service_client() -> Optional[Client]:
    global _service_client
    if _service_client is not None:
        return _service_client
    if settings.SUPABASE_SERVICE_KEY:
        try:
            _service_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        except Exception as e:
            logger.warning(f"Service client not initialized: {e}")
    return _service_client
