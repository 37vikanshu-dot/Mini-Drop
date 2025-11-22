import os
from supabase import create_client, Client
import logging

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")
supabase: Client | None = None
try:
    if url and key:
        supabase = create_client(url, key)
    else:
        logging.warning("Supabase URL or Key not found in environment variables.")
except Exception as e:
    logging.exception(f"Failed to initialize Supabase client: {e}")


def get_supabase() -> Client | None:
    return supabase