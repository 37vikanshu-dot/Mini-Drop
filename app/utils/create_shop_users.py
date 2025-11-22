import asyncio
import logging
import os
import sys
import uuid

sys.path.append(os.getcwd())
from app.utils.supabase_client import get_supabase
from app.utils.auth import hash_password


async def create_shop_users():
    supabase = get_supabase()
    if not supabase:
        print(
            "❌ Could not connect to Supabase. Please check your environment variables."
        )
        return
    print("🔄 Fetching shops...")
    try:
        response = supabase.table("shops").select("*").execute()
        shops = response.data
        if not shops:
            print("⚠️ No shops found.")
            return
        print(f"✅ Found {len(shops)} shops. Creating/Updating user accounts...")
        for shop in shops:
            shop_id = shop["id"]
            shop_name = shop["name"]
            slug = (
                shop_name.lower().replace(" ", "").replace("'", "").replace("&", "and")
            )
            email = f"{slug}@minidrop.com"
            password = "shop123"
            hashed_pw = hash_password(password)
            print(f"   Checking user for {shop_name} ({email})...")
            user_res = supabase.table("users").select("*").eq("email", email).execute()
            if user_res.data:
                user = user_res.data[0]
                user_id = user["id"]
                print(f"   ℹ️ User exists (ID: {user_id}). Updating shop_id...")
                supabase.table("users").update(
                    {"shop_id": shop_id, "role": "shop_owner"}
                ).eq("id", user_id).execute()
            else:
                new_id = str(uuid.uuid4())
                new_user = {
                    "id": new_id,
                    "name": f"{shop_name} Owner",
                    "email": email,
                    "role": "shop_owner",
                    "password_hash": hashed_pw,
                    "shop_id": shop_id,
                    "phone": "",
                }
                supabase.table("users").insert(new_user).execute()
                print(f"   ✅ Created new user for {shop_name}")
        print("""
🎉 Shop users generation complete!""")
        print("   Default password for all shop accounts: shop123")
    except Exception as e:
        logging.exception(f"Error creating shop users: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(create_shop_users())