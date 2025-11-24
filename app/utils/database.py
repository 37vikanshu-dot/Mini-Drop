import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Optional
from app.utils.supabase_client import get_supabase


class DatabaseManager:
    """Database operations manager for both Supabase and direct SQL queries."""

    def __init__(self):
        self.supabase = get_supabase()
        self.engine = None
        self._setup_engine()

    def _setup_engine(self):
        """Set up SQLAlchemy engine if REFLEX_DB_URL is available."""
        db_url = os.environ.get("REFLEX_DB_URL")
        if db_url:
            try:
                self.engine = create_engine(db_url)
                self.Session = sessionmaker(bind=self.engine)
                logging.info("Database engine initialized successfully")
            except Exception as e:
                logging.exception(f"Failed to initialize database engine: {e}")

    async def execute_query(
        self, query: str, params: dict = None
    ) -> list[dict[str, object]]:
        """Execute a raw SQL query safely."""
        if not self.engine:
            logging.error("Database engine not available")
            return []
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                return [dict(row._mapping) for row in result]
        except Exception as e:
            logging.exception(f"Database query error: {e}")
            return []

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email from database."""
        if not self.supabase:
            return None
        try:
            response = (
                self.supabase.table("users").select("*").eq("email", email).execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Error fetching user by email: {e}")
            return None

    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID from database."""
        if not self.supabase:
            return None
        try:
            response = (
                self.supabase.table("users").select("*").eq("id", user_id).execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Error fetching user by ID: {e}")
            return None

    async def create_user(self, user_data: dict) -> Optional[dict]:
        """Create a new user in the database."""
        if not self.supabase:
            return None
        try:
            response = self.supabase.table("users").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Error creating user: {e}")
            return None

    async def get_shops(self, category_slug: Optional[str] = None) -> list[dict]:
        """Get shops from database."""
        if not self.supabase:
            return []
        try:
            query = self.supabase.table("shops").select("*").eq("is_active", True)
            if category_slug and category_slug != "all":
                query = query.eq("category_slug", category_slug)
            response = query.execute()
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching shops: {e}")
            return []

    async def get_products(self, shop_id: Optional[int] = None) -> list[dict]:
        """Get products from database."""
        if not self.supabase:
            return []
        try:
            query = self.supabase.table("products").select("*").eq("is_available", True)
            if shop_id:
                query = query.eq("shop_id", shop_id)
            response = query.execute()
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching products: {e}")
            return []

    async def get_categories(self, include_inactive: bool = False) -> list[dict]:
        """Get categories from database."""
        if not self.supabase:
            return []
        try:
            query = self.supabase.table("categories").select("*")
            if not include_inactive:
                query = query.eq("is_active", True)
            response = query.order("sort_order").execute()
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching categories: {e}")
            return []

    async def create_category(self, category_data: dict) -> Optional[dict]:
        """Create a new category."""
        if not self.supabase:
            return None
        try:
            response = self.supabase.table("categories").insert(category_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Error creating category: {e}")
            return None

    async def update_category(self, category_id: int, updates: dict) -> bool:
        """Update a category."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("categories").update(updates).eq(
                "id", category_id
            ).execute()
            return True
        except Exception as e:
            logging.exception(f"Error updating category: {e}")
            return False

    async def delete_category(self, category_id: int) -> bool:
        """Delete a category."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("categories").delete().eq("id", category_id).execute()
            return True
        except Exception as e:
            logging.exception(f"Error deleting category: {e}")
            return False

    async def create_order(self, order_data: dict) -> Optional[dict]:
        """Create a new order in the database."""
        if not self.supabase:
            return None
        try:
            response = self.supabase.table("orders").insert(order_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Error creating order: {e}")
            return None

    async def create_order_items(self, items_data: list[dict]) -> bool:
        """Create order items in the database."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("order_items").insert(items_data).execute()
            return True
        except Exception as e:
            logging.exception(f"Error creating order items: {e}")
            return False

    async def get_orders_by_user(self, user_id: str) -> list[dict]:
        """Get orders for a specific user."""
        if not self.supabase:
            return []
        try:
            response = (
                self.supabase.table("orders")
                .select("*, order_items(*)")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching user orders: {e}")
            return []

    async def get_orders_by_shop(self, shop_id: int) -> list[dict]:
        """Get orders for a specific shop."""
        if not self.supabase:
            return []
        try:
            response = (
                self.supabase.table("orders")
                .select("*, order_items(*)")
                .eq("shop_id", shop_id)
                .order("created_at", desc=True)
                .execute()
            )
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching shop orders: {e}")
            return []

    async def update_order_status(self, order_id: str, status: str) -> bool:
        """Update the status of an order."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("orders").update({"status": status}).eq(
                "id", order_id
            ).execute()
            return True
        except Exception as e:
            logging.exception(f"Error updating order status: {e}")
            return False

    async def get_available_orders(self) -> list[dict]:
        """Get all orders that are ready for pickup."""
        if not self.supabase:
            return []
        try:
            response = (
                self.supabase.table("orders")
                .select("*, order_items(*)")
                .eq("status", "Ready")
                .order("created_at", desc=True)
                .execute()
            )
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching available orders: {e}")
            return []

    async def get_rider_orders(self, rider_id: str) -> list[dict]:
        """Get orders assigned to a specific rider."""
        if not self.supabase:
            return []
        try:
            response = (
                self.supabase.table("orders")
                .select("*, order_items(*)")
                .eq("rider_id", rider_id)
                .order("created_at", desc=True)
                .execute()
            )
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching rider orders: {e}")
            return []

    async def assign_order_to_rider(self, order_id: str, rider_id: str) -> bool:
        """Assign an order to a rider and update status."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("orders").update(
                {"rider_id": rider_id, "status": "Out for Delivery"}
            ).eq("id", order_id).execute()
            return True
        except Exception as e:
            logging.exception(f"Error assigning order: {e}")
            return False

    async def get_rider_by_id(self, rider_id: str) -> dict | None:
        """Get rider details by ID."""
        if not self.supabase:
            return None
        try:
            response = (
                self.supabase.table("riders").select("*").eq("id", rider_id).execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Error fetching rider: {e}")
            return None

    async def update_rider_earnings(self, rider_id: str, amount: float) -> bool:
        """Update rider earnings and completed orders count."""
        if not self.supabase:
            return False
        try:
            rider = await self.get_rider_by_id(rider_id)
            if not rider:
                return False
            current_earnings = rider.get("earnings", 0.0)
            current_completed = rider.get("completed_orders", 0)
            updates = {
                "earnings": current_earnings + amount,
                "completed_orders": current_completed + 1,
            }
            self.supabase.table("riders").update(updates).eq("id", rider_id).execute()
            return True
        except Exception as e:
            logging.exception(f"Error updating rider stats: {e}")
            return False

    async def toggle_rider_status(self, rider_id: str, status: str) -> bool:
        """Update rider online/offline status."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("riders").update({"status": status}).eq(
                "id", rider_id
            ).execute()
            return True
        except Exception as e:
            logging.exception(f"Error updating rider status: {e}")
            return False

    async def get_riders(self) -> list[dict]:
        """Get all riders from database."""
        if not self.supabase:
            return []
        try:
            response = self.supabase.table("riders").select("*").execute()
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching riders: {e}")
            return []

    async def get_coupons(self) -> list[dict]:
        """Get all coupons from database."""
        if not self.supabase:
            return []
        try:
            response = self.supabase.table("coupons").select("*").execute()
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching coupons: {e}")
            return []

    async def get_all_orders(self) -> list[dict]:
        """Get all orders for admin view."""
        if not self.supabase:
            return []
        try:
            response = (
                self.supabase.table("orders")
                .select("*, order_items(*)")
                .order("created_at", desc=True)
                .execute()
            )
            return response.data or []
        except Exception as e:
            logging.exception(f"Error fetching all orders: {e}")
            return []

    async def create_shop(self, shop_data: dict) -> Optional[dict]:
        """Create a new shop."""
        if not self.supabase:
            return None
        try:
            response = self.supabase.table("shops").insert(shop_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Error creating shop: {e}")
            return None

    async def update_shop(self, shop_id: int, updates: dict) -> bool:
        """Update a shop."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("shops").update(updates).eq("id", shop_id).execute()
            return True
        except Exception as e:
            logging.exception(f"Error updating shop: {e}")
            return False

    async def delete_shop(self, shop_id: int) -> bool:
        """Delete a shop."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("shops").delete().eq("id", shop_id).execute()
            return True
        except Exception as e:
            logging.exception(f"Error deleting shop: {e}")
            return False

    async def create_rider(self, rider_data: dict) -> Optional[dict]:
        """Create a new rider."""
        if not self.supabase:
            return None
        try:
            response = self.supabase.table("riders").insert(rider_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Error creating rider: {e}")
            return None

    async def create_product(self, product_data: dict) -> Optional[dict]:
        """Create a new product."""
        if not self.supabase:
            return None
        try:
            response = self.supabase.table("products").insert(product_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.exception(f"Error creating product: {e}")
            return None

    async def update_product(self, product_id: int, updates: dict) -> bool:
        """Update a product."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("products").update(updates).eq(
                "id", product_id
            ).execute()
            return True
        except Exception as e:
            logging.exception(f"Error updating product: {e}")
            return False

    async def toggle_product_stock(self, product_id: int, new_status: bool) -> bool:
        """Toggle product availability."""
        if not self.supabase:
            return False
        try:
            self.supabase.table("products").update({"is_available": new_status}).eq(
                "id", product_id
            ).execute()
            return True
        except Exception as e:
            logging.exception(f"Error toggling product stock: {e}")
            return False