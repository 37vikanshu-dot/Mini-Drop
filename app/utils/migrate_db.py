import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.getcwd())
try:
    from app.utils.auth import hash_password
except ImportError:
    logging.exception(
        "Failed to import hash_password from current path. Attempting to adjust path."
    )
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    from app.utils.auth import hash_password
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
SCHEMA_SQL = """
-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    icon TEXT,
    color_bg TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0
);

-- Create shops table
CREATE TABLE IF NOT EXISTS shops (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_slug TEXT,
    rating DECIMAL(2,1) DEFAULT 5.0,
    delivery_time TEXT,
    distance TEXT,
    image_url TEXT,
    address TEXT,
    is_featured BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    role TEXT DEFAULT 'customer',
    password_hash TEXT NOT NULL,
    avatar_url TEXT,
    shop_id INTEGER REFERENCES shops(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    shop_id INTEGER REFERENCES shops(id),
    name TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2),
    image_url TEXT,
    description TEXT,
    is_available BOOLEAN DEFAULT TRUE,
    unit TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    subtotal DECIMAL(10,2) NOT NULL,
    delivery_fee DECIMAL(10,2) DEFAULT 15.0,
    total_amount DECIMAL(10,2) NOT NULL,
    status TEXT DEFAULT 'Pending',
    date TEXT,
    time TEXT,
    delivery_address TEXT,
    payment_method TEXT,
    shop_id INTEGER REFERENCES shops(id),
    status TEXT,
    rider_id TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id TEXT REFERENCES orders(id),
    product_id INTEGER,
    name TEXT,
    price DECIMAL(10,2),
    quantity INTEGER,
    image_url TEXT
);

-- Create riders table
CREATE TABLE IF NOT EXISTS riders (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    vehicle_type TEXT,
    status TEXT DEFAULT 'Offline',
    earnings DECIMAL(10,2) DEFAULT 0,
    completed_orders INTEGER DEFAULT 0
);

-- Create coupons table
CREATE TABLE IF NOT EXISTS coupons (
    code TEXT PRIMARY KEY,
    discount DECIMAL(10,2),
    type TEXT,
    min_order DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create addresses table
CREATE TABLE IF NOT EXISTS addresses (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    type TEXT,
    address TEXT,
    phone TEXT
);

-- Create payouts table
CREATE TABLE IF NOT EXISTS payouts (
    id TEXT PRIMARY KEY,
    date TEXT,
    order_id TEXT,
    order_amount DECIMAL(10,2),
    commission DECIMAL(10,2),
    payout_amount DECIMAL(10,2),
    status TEXT
);

-- Add columns if they don't exist (migrations)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'orders' AND column_name = 'rider_id') THEN
        ALTER TABLE orders ADD COLUMN rider_id TEXT;
    END IF;
END $$;
"""


def print_setup_instructions():
    """Print clear instructions on how to get the DB URL."""
    print(
        """
"""
        + "=" * 60
    )
    print("❌ DATABASE CONNECTION STRING MISSING")
    print("=" * 60)
    print("""
To set up your database, you need to provide a connection string.""")
    print("""
1. Go to your Supabase Project Dashboard: https://supabase.com/dashboard""")
    print("2. Navigate to: Project Settings -> Database -> Connection String -> URI")
    print("3. Copy the connection string (it starts with postgresql://...)")
    print("4. Replace '[YOUR-PASSWORD]' with your actual database password")
    print("5. Set the environment variable in your terminal:")
    print("""
   export REFLEX_DB_URL='postgresql://postgres.xxxx:password@aws-0-region.pooler.supabase.com:6543/postgres'""")
    print("""
   OR""")
    print("""
   export DATABASE_URL='...
""")
    print(
        "=" * 60
        + """
"""
    )


def print_manual_sql_instructions(error_msg):
    """Print the SQL schema for manual execution."""
    print(
        """
"""
        + "=" * 60
    )
    print("⚠️  DATABASE MIGRATION FAILED")
    print("=" * 60)
    print(f"\nError: {error_msg}")
    print("""
If you cannot connect from this script, you can run the SQL schema manually:""")
    print("1. Go to Supabase Dashboard -> SQL Editor")
    print("2. Click 'New Query'")
    print("3. Copy and paste the following SQL:")
    print(
        """
"""
        + "-" * 20
        + " COPY BELOW "
        + "-" * 20
    )
    print(SCHEMA_SQL)
    print("-" * 20 + " COPY ABOVE " + "-" * 20)
    print(
        """
"""
        + "=" * 60
        + """
"""
    )


def run_migration():
    """Run the database migration and seeding."""
    db_url = os.environ.get("REFLEX_DB_URL") or os.environ.get("DATABASE_URL")
    if not db_url:
        print_setup_instructions()
        return
    masked_url = db_url.split("@")[-1] if "@" in db_url else "..."
    logging.info(f"Attempting to connect to database at {masked_url}")
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            logging.info("Connected! Creating tables...")
            conn.execute(text(SCHEMA_SQL))
            conn.commit()
            logging.info("✅ Tables structure applied successfully.")
            logging.info("Seeding sample data...")
            users_data = [
                (
                    "user_001",
                    "Admin User",
                    "admin@minidrop.com",
                    "9999999999",
                    "admin",
                    hash_password("password123"),
                ),
                (
                    "user_002",
                    "Shop Owner",
                    "owner@freshmart.com",
                    "8888888888",
                    "shop_owner",
                    hash_password("password123"),
                ),
                (
                    "user_003",
                    "John Doe",
                    "customer@example.com",
                    "7777777777",
                    "customer",
                    hash_password("password123"),
                ),
            ]
            for user in users_data:
                try:
                    conn.execute(
                        text("""
                            INSERT INTO users (id, name, email, phone, role, password_hash) 
                            VALUES (:id, :name, :email, :phone, :role, :password_hash)
                            ON CONFLICT (email) DO NOTHING
                        """),
                        {
                            "id": user[0],
                            "name": user[1],
                            "email": user[2],
                            "phone": user[3],
                            "role": user[4],
                            "password_hash": user[5],
                        },
                    )
                except Exception as e:
                    logging.exception(f"Failed to insert user {user[2]}: {e}")
            categories_data = [
                ("Groceries", "grocery", "shopping-basket", "bg-green-100", 1),
                ("Snacks", "snacks", "cookie", "bg-orange-100", 2),
                ("Dairy", "dairy", "milk", "bg-blue-100", 3),
                ("Medicines", "medical", "pill", "bg-red-100", 4),
                ("Stationery", "stationery", "pencil", "bg-yellow-100", 5),
                ("Bakery", "bakery", "croissant", "bg-amber-100", 6),
            ]
            for cat in categories_data:
                conn.execute(
                    text("""
                        INSERT INTO categories (name, slug, icon, color_bg, sort_order)
                        VALUES (:name, :slug, :icon, :color_bg, :sort_order)
                        ON CONFLICT (slug) DO NOTHING
                    """),
                    {
                        "name": cat[0],
                        "slug": cat[1],
                        "icon": cat[2],
                        "color_bg": cat[3],
                        "sort_order": cat[4],
                    },
                )
            shops_data = [
                (
                    "Fresh Mart Grocery",
                    "grocery",
                    4.8,
                    "15-20 min",
                    "0.8 km",
                    "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=400&q=80",
                    "12 Main St",
                    True,
                ),
                (
                    "City Medicos",
                    "medical",
                    4.5,
                    "10-15 min",
                    "0.5 km",
                    "https://images.unsplash.com/photo-1585435557343-3b092031a831?auto=format&fit=crop&w=400&q=80",
                    "45 Park Ave",
                    True,
                ),
                (
                    "Daily Dairy Needs",
                    "dairy",
                    4.9,
                    "10 min",
                    "0.2 km",
                    "https://images.unsplash.com/photo-1628088062854-d1870b4553da?auto=format&fit=crop&w=400&q=80",
                    "88 Market Rd",
                    False,
                ),
                (
                    "Student Stationers",
                    "stationery",
                    4.2,
                    "25-30 min",
                    "1.5 km",
                    "https://images.unsplash.com/photo-1550399105-c4db5fb85c18?auto=format&fit=crop&w=400&q=80",
                    "University Sq",
                    False,
                ),
                (
                    "Oven Fresh Bakery",
                    "bakery",
                    4.7,
                    "20-25 min",
                    "1.2 km",
                    "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&q=80",
                    "Baker St",
                    True,
                ),
            ]
            for shop in shops_data:
                existing = conn.execute(
                    text("SELECT id FROM shops WHERE name = :name"), {"name": shop[0]}
                ).fetchone()
                if not existing:
                    conn.execute(
                        text("""
                            INSERT INTO shops (name, category_slug, rating, delivery_time, distance, image_url, address, is_featured)
                            VALUES (:name, :category_slug, :rating, :delivery_time, :distance, :image_url, :address, :is_featured)
                        """),
                        {
                            "name": shop[0],
                            "category_slug": shop[1],
                            "rating": shop[2],
                            "delivery_time": shop[3],
                            "distance": shop[4],
                            "image_url": shop[5],
                            "address": shop[6],
                            "is_featured": shop[7],
                        },
                    )
            shop_map = {}
            result = conn.execute(text("SELECT name, id FROM shops"))
            for row in result:
                shop_map[row[0]] = row[1]
            products_data = [
                (
                    "Full Cream Milk",
                    32.0,
                    35.0,
                    "https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=200&q=80",
                    "Fresh full cream milk",
                    "1 L",
                    "Fresh Mart Grocery",
                ),
                (
                    "Whole Wheat Bread",
                    45.0,
                    50.0,
                    "https://images.unsplash.com/photo-1598373182133-52452f7691ef?auto=format&fit=crop&w=200&q=80",
                    "Freshly baked brown bread",
                    "400g",
                    "Fresh Mart Grocery",
                ),
                (
                    "Farm Eggs",
                    65.0,
                    75.0,
                    "https://images.unsplash.com/photo-1506976785307-8732e854ad03?auto=format&fit=crop&w=200&q=80",
                    "Pack of 6 fresh eggs",
                    "6 pcs",
                    "Fresh Mart Grocery",
                ),
                (
                    "Maggie Noodles",
                    14.0,
                    15.0,
                    "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?auto=format&fit=crop&w=200&q=80",
                    "Instant noodles",
                    "70g",
                    "Fresh Mart Grocery",
                ),
                (
                    "Paracetamol 500mg",
                    20.0,
                    22.0,
                    "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=200&q=80",
                    "Fever reducer",
                    "Strip of 10",
                    "City Medicos",
                ),
                (
                    "Cotton Bandage",
                    30.0,
                    35.0,
                    "https://images.unsplash.com/photo-1583947215259-38e31be8751f?auto=format&fit=crop&w=200&q=80",
                    "Sterile bandage",
                    "1 Roll",
                    "City Medicos",
                ),
                (
                    "Lays Classic Salted",
                    20.0,
                    20.0,
                    "https://images.unsplash.com/photo-1566478919030-2609e87011bc?auto=format&fit=crop&w=200&q=80",
                    "Classic potato chips",
                    "50g",
                    "Fresh Mart Grocery",
                ),
                (
                    "Ballpoint Pen Blue",
                    10.0,
                    12.0,
                    "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?auto=format&fit=crop&w=200&q=80",
                    "Smooth writing pen",
                    "1 pc",
                    "Student Stationers",
                ),
                (
                    "Spiral Notebook",
                    55.0,
                    60.0,
                    "https://images.unsplash.com/photo-1531346878377-a516a63156a5?auto=format&fit=crop&w=200&q=80",
                    "100 pages ruled",
                    "1 pc",
                    "Student Stationers",
                ),
            ]
            for prod in products_data:
                shop_name = prod[6]
                if shop_name in shop_map:
                    shop_id = shop_map[shop_name]
                    existing = conn.execute(
                        text(
                            "SELECT id FROM products WHERE name = :name AND shop_id = :shop_id"
                        ),
                        {"name": prod[0], "shop_id": shop_id},
                    ).fetchone()
                    if not existing:
                        conn.execute(
                            text("""
                                INSERT INTO products (shop_id, name, price, original_price, image_url, description, unit, is_available)
                                VALUES (:shop_id, :name, :price, :original_price, :image_url, :description, :unit, TRUE)
                            """),
                            {
                                "shop_id": shop_id,
                                "name": prod[0],
                                "price": prod[1],
                                "original_price": prod[2],
                                "image_url": prod[3],
                                "description": prod[4],
                                "unit": prod[5],
                            },
                        )
            riders_data = [
                ("r1", "Rahul Kumar", "9876543210", "Bike"),
                ("r2", "Amit Singh", "9876543211", "Scooter"),
            ]
            for rider in riders_data:
                conn.execute(
                    text("""
                        INSERT INTO riders (id, name, phone, vehicle_type, status, earnings, completed_orders)
                        VALUES (:id, :name, :phone, :vehicle_type, 'Online', 0, 0)
                        ON CONFLICT (id) DO NOTHING
                    """),
                    {
                        "id": rider[0],
                        "name": rider[1],
                        "phone": rider[2],
                        "vehicle_type": rider[3],
                    },
                )
            coupons_data = [
                ("WELCOME50", 50.0, "Flat", 200.0),
                ("FRESH20", 20.0, "Percent", 500.0),
            ]
            for coupon in coupons_data:
                conn.execute(
                    text("""
                        INSERT INTO coupons (code, discount, type, min_order, is_active)
                        VALUES (:code, :discount, :type, :min_order, TRUE)
                        ON CONFLICT (code) DO NOTHING
                    """),
                    {
                        "code": coupon[0],
                        "discount": coupon[1],
                        "type": coupon[2],
                        "min_order": coupon[3],
                    },
                )
            conn.commit()
            logging.info("✅ Sample data seeded successfully!")
    except SQLAlchemyError as e:
        logging.exception(f"❌ Database error: {e}")
        print_manual_sql_instructions(e)
    except Exception as e:
        logging.exception(f"❌ An error occurred: {e}")
        print_manual_sql_instructions(e)


if __name__ == "__main__":
    run_migration()