import asyncio
import logging
import os
import sys

sys.path.append(os.getcwd())
from app.utils.supabase_client import get_supabase
from app.utils.db_seed import seed_admin_user


async def reset_database(create_admin=True):
    supabase = get_supabase()
    if not supabase:
        print(
            "❌ Could not connect to Supabase. Please check your environment variables."
        )
        return
    print("""🗑️  Clearing all data from database...
""")

    def clear_table(table_name, id_col="id", is_int=False):
        try:
            query = supabase.table(table_name).delete()
            if is_int:
                result = query.gte(id_col, 0).execute()
            else:
                result = query.neq(id_col, "xxxxx").execute()
            count = len(result.data) if result.data else 0
            print(f"✅ Cleared {table_name}: {count} rows")
        except Exception as e:
            logging.exception(f"Error clearing {table_name}: {e}")
            print(f"⚠️  {table_name}: {str(e)[:100]}")

    clear_table("order_items", is_int=True)
    clear_table("payouts", is_int=False)
    clear_table("addresses", is_int=False)
    clear_table("orders", is_int=False)
    clear_table("products", is_int=True)
    clear_table("shops", is_int=True)
    clear_table("categories", is_int=True)
    clear_table("coupons", id_col="code", is_int=False)
    clear_table("riders", is_int=False)
    clear_table("users", is_int=False)
    print(
        """
"""
        + "=" * 60
    )
    print("✅ DATABASE RESET COMPLETE!")
    print("=" * 60)
    if create_admin:
        print("""
👤 Creating default admin user...""")
        await seed_admin_user()
        print("✅ Default admin user created!")
        print("   Email: admin@minidrop.com")
        print("   Password: password123")
    print("""
Next steps:""")
    print("1. Log in as admin to configure your store")
    print("2. Add categories and shops")
    print("3. Add products to shops")


if __name__ == "__main__":
    asyncio.run(reset_database())