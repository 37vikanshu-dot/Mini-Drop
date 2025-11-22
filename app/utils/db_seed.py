import logging
from app.utils.supabase_client import get_supabase
from app.utils.auth import hash_password


def seed_database():
    """Mock database seeding - No operation required."""
    pass


async def seed_admin_user(
    email: str = "admin@minidrop.com", password: str = "password123"
):
    """Create an initial admin user if one doesn't exist."""
    supabase = get_supabase()
    if not supabase:
        logging.error("Supabase client not available for seeding.")
        return
    try:
        response = supabase.table("users").select("email").eq("email", email).execute()
        if response.data:
            logging.info(f"User {email} already exists. Skipping creation.")
            return
        user_id = "user_admin_init"
        user_data = {
            "id": user_id,
            "name": "System Admin",
            "email": email,
            "phone": "0000000000",
            "role": "admin",
            "password_hash": hash_password(password),
        }
        supabase.table("users").insert(user_data).execute()
        logging.info(f"Successfully created admin user: {email}")
    except Exception as e:
        logging.exception(f"Error seeding admin user: {e}")