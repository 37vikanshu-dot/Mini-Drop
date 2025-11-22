import asyncio
import logging
import os
import sys
from app.utils.supabase_client import get_supabase
from app.utils.db_seed import seed_admin_user
from app.utils.migrate_db import run_migration


def print_header():
    print("=" * 60)
    print("🛠️  Mini Drop Database Manager")
    print("=" * 60)


async def get_stats():
    supabase = get_supabase()
    if not supabase:
        print("❌ Could not connect to Supabase.")
        return
    tables = [
        "users",
        "shops",
        "products",
        "categories",
        "orders",
        "order_items",
        "riders",
        "coupons",
        "payouts",
        "addresses",
    ]
    print("""
📊 Database Statistics:""")
    print("-" * 40)
    print(f"{'Table':<20} | {'Count':<10}")
    print("-" * 40)
    for table in tables:
        try:
            res = supabase.table(table).select("*", count="exact", head=True).execute()
            count = res.count
            print(f"{table:<20} | {count:<10}")
        except Exception as e:
            logging.exception(f"Error getting stats for {table}: {e}")
            print(f"{table:<20} | Error")
    print(
        "-" * 40
        + """
"""
    )


async def clear_database():
    supabase = get_supabase()
    if not supabase:
        print("❌ Could not connect to Supabase.")
        return
    print("""
⚠️  WARNING: This will DELETE ALL DATA from the database.""")
    confirm = input("Are you sure you want to continue? (yes/no): ")
    if confirm.lower() != "yes":
        print("Operation cancelled.")
        return
    print("""
🗑️  Clearing all data...""")
    tables_config = [
        ("order_items", True),
        ("payouts", False),
        ("addresses", False),
        ("orders", False),
        ("products", True),
        ("shops", True),
        ("categories", True),
        ("coupons", False, "code"),
        ("riders", False),
        ("users", False),
    ]
    for config in tables_config:
        table = config[0]
        is_int = config[1]
        id_col = config[2] if len(config) > 2 else "id"
        try:
            query = supabase.table(table).delete()
            if is_int:
                query.gte(id_col, 0).execute()
            else:
                query.neq(id_col, "xxxxx").execute()
            print(f"✅ Cleared {table}")
        except Exception as e:
            logging.exception(f"Failed to clear {table}: {e}")
            print(f"⚠️  Failed to clear {table}: {e}")
    print("""
✅ Database cleared successfully!""")


async def seed_admin():
    print("""
👤 Creating admin user...""")
    await seed_admin_user()
    print("✅ Admin user creation process complete.")


def seed_sample_data():
    print("""
🌱 Seeding sample data via SQLAlchemy...""")
    try:
        run_migration()
        print("✅ Sample data seeding process finished.")
    except Exception as e:
        logging.exception(f"Failed to seed data: {e}")
        print(f"❌ Failed to seed data: {e}")


async def main_menu():
    while True:
        print_header()
        print("1. Reset Database (Clear all data)")
        print("2. Reset & Create Admin User")
        print("3. Seed Sample Data (Categories, Shops, Products)")
        print("4. View Database Statistics")
        print("5. Exit")
        choice = input("""
👉 Select an option (1-5): """)
        if choice == "1":
            await clear_database()
        elif choice == "2":
            await clear_database()
            await seed_admin()
        elif choice == "3":
            seed_sample_data()
        elif choice == "4":
            await get_stats()
        elif choice == "5":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid option. Please try again.")
        input("""
Press Enter to continue...""")


if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt as e:
        logging.exception(f"Interrupted: {e}")
        print("""
Exiting...""")