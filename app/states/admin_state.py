import reflex as rx
from app.data import (
    ShopDict,
    OrderDict,
    RiderDict,
    CouponDict,
    WeeklyStatDict,
    CategoryDict,
)
import app.data as data
from app.utils.database import DatabaseManager
import logging
import random


class AdminState(rx.State):
    shops: list[ShopDict] = []
    categories: list[CategoryDict] = []
    orders: list[OrderDict] = []
    riders: list[RiderDict] = []
    pricing_config: data.PricingConfigDict = data.PRICING_CONFIG
    coupons: list[CouponDict] = []
    revenue_stats: list[WeeklyStatDict] = [
        {"day": "Mon", "revenue": 0, "orders": 0},
        {"day": "Tue", "revenue": 0, "orders": 0},
        {"day": "Wed", "revenue": 0, "orders": 0},
        {"day": "Thu", "revenue": 0, "orders": 0},
        {"day": "Fri", "revenue": 0, "orders": 0},
        {"day": "Sat", "revenue": 0, "orders": 0},
        {"day": "Sun", "revenue": 0, "orders": 0},
    ]
    is_shop_dialog_open: bool = False
    editing_shop_id: int = 0
    shop_form_name: str = ""
    shop_form_category: str = ""
    shop_form_address: str = ""
    shop_form_image_url: str = ""
    shop_form_commission: str = "10"
    is_rider_dialog_open: bool = False
    rider_form_name: str = ""
    rider_form_phone: str = ""
    rider_form_vehicle: str = "Bike"
    is_category_dialog_open: bool = False
    editing_category_id: int = 0
    category_form_name: str = ""
    category_form_slug: str = ""
    category_form_icon: str = "circle"
    category_form_color: str = "bg-gray-100"

    @rx.event
    async def on_mount(self):
        await self.fetch_data()

    @rx.event
    async def fetch_data(self):
        db = DatabaseManager()
        if db.supabase:
            self.shops = await db.get_shops()
            self.riders = await db.get_riders()
            self.coupons = await db.get_coupons()
            self.categories = await db.get_categories(include_inactive=True)
            db_orders = await db.get_all_orders()
            processed_orders = []
            for o in db_orders:
                o["items"] = o.pop("order_items", [])
                processed_orders.append(o)
            self.orders = processed_orders
        else:
            self.shops = data.SHOPS
            self.riders = data.RIDERS
            self.coupons = data.COUPONS
            self.categories = data.CATEGORIES
            self.orders = data.ORDERS

    @rx.var
    def total_orders_today(self) -> int:
        return 256

    @rx.var
    def total_earnings(self) -> float:
        return 15400.0

    @rx.var
    def active_riders_count(self) -> int:
        return len([r for r in self.riders if r["status"] == "Online"])

    @rx.event
    def open_add_shop_dialog(self):
        self.editing_shop_id = 0
        self.shop_form_name = ""
        self.shop_form_category = ""
        self.shop_form_address = ""
        self.shop_form_image_url = ""
        self.shop_form_commission = "10"
        self.is_shop_dialog_open = True

    @rx.event
    def open_edit_shop_dialog(self, shop: ShopDict):
        self.editing_shop_id = shop["id"]
        self.shop_form_name = shop["name"]
        self.shop_form_category = shop["category_slug"]
        self.shop_form_address = shop["address"]
        self.shop_form_image_url = shop["image_url"]
        self.shop_form_commission = "10"
        self.is_shop_dialog_open = True

    @rx.event
    async def delete_shop(self, shop_id: int):
        db = DatabaseManager()
        if db.supabase:
            success = await db.delete_shop(shop_id)
            if success:
                await self.fetch_data()
                return rx.toast("Shop deleted successfully")
            else:
                return rx.toast.error("Failed to delete shop")
        else:
            return rx.toast.error("Database connection required")

    @rx.event
    def close_shop_dialog(self):
        self.is_shop_dialog_open = False

    @rx.event
    def set_shop_dialog_open(self, value: bool):
        self.is_shop_dialog_open = value

    @rx.event
    async def save_shop(self):
        db = DatabaseManager()
        if self.editing_shop_id == 0:
            new_shop = {
                "name": self.shop_form_name,
                "category_slug": self.shop_form_category,
                "rating": 5.0,
                "delivery_time": "30-45 min",
                "distance": "1.0 km",
                "image_url": self.shop_form_image_url
                or "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=400&q=80",
                "address": self.shop_form_address or "New Address",
                "is_featured": False,
            }
            await db.create_shop(new_shop)
            rx.toast("Shop created successfully")
        else:
            updates = {
                "name": self.shop_form_name,
                "category_slug": self.shop_form_category,
                "address": self.shop_form_address,
                "image_url": self.shop_form_image_url,
            }
            await db.update_shop(self.editing_shop_id, updates)
            rx.toast("Shop updated successfully")
        self.is_shop_dialog_open = False
        await self.fetch_data()

    @rx.event
    def open_add_rider_dialog(self):
        self.rider_form_name = ""
        self.rider_form_phone = ""
        self.rider_form_vehicle = "Bike"
        self.is_rider_dialog_open = True

    @rx.event
    def set_rider_dialog_open(self, value: bool):
        self.is_rider_dialog_open = value

    @rx.event
    async def save_rider(self):
        db = DatabaseManager()
        new_rider = {
            "id": f"r{random.randint(1000, 9999)}",
            "name": self.rider_form_name,
            "phone": self.rider_form_phone,
            "vehicle_type": self.rider_form_vehicle,
            "status": "Offline",
            "earnings": 0.0,
            "completed_orders": 0,
        }
        await db.create_rider(new_rider)
        self.is_rider_dialog_open = False
        await self.fetch_data()
        return rx.toast("Rider added successfully")

    @rx.event
    async def toggle_rider_status(self, rider_id: str):
        await self.fetch_data()

    @rx.event
    def update_delivery_base(self, value: str):
        try:
            self.pricing_config["delivery_base"] = float(value)
            data.PRICING_CONFIG["delivery_base"] = float(value)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def update_surge_multiplier(self, value: str):
        try:
            self.pricing_config["surge_multiplier"] = float(value)
            data.PRICING_CONFIG["surge_multiplier"] = float(value)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def update_platform_fee(self, value: str):
        try:
            val = float(value)
            self.pricing_config["platform_fee"] = val
            data.PRICING_CONFIG["platform_fee"] = val
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def update_gst_percent(self, value: str):
        try:
            val = float(value)
            self.pricing_config["gst_percent"] = val
            data.PRICING_CONFIG["gst_percent"] = val
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def toggle_surge_active(self, value: bool):
        self.pricing_config["is_surge_active"] = value
        data.PRICING_CONFIG["is_surge_active"] = value

    @rx.event
    def set_shop_form_name(self, val: str):
        self.shop_form_name = val

    @rx.event
    def set_shop_form_category(self, val: str):
        self.shop_form_category = val

    @rx.event
    def set_shop_form_address(self, val: str):
        self.shop_form_address = val

    @rx.event
    def set_shop_form_image_url(self, val: str):
        self.shop_form_image_url = val

    @rx.event
    def set_shop_form_commission(self, val: str):
        self.shop_form_commission = val

    @rx.event
    def set_rider_form_name(self, val: str):
        self.rider_form_name = val

    @rx.event
    def set_rider_form_phone(self, val: str):
        self.rider_form_phone = val

    @rx.event
    def set_rider_form_vehicle(self, val: str):
        self.rider_form_vehicle = val

    @rx.event
    def open_add_category_dialog(self):
        self.editing_category_id = 0
        self.category_form_name = ""
        self.category_form_slug = ""
        self.category_form_icon = "shopping-basket"
        self.category_form_color = "bg-gray-100"
        self.is_category_dialog_open = True

    @rx.event
    def open_edit_category_dialog(self, category: CategoryDict):
        self.editing_category_id = category["id"]
        self.category_form_name = category["name"]
        self.category_form_slug = category["slug"]
        self.category_form_icon = category.get("icon", "circle")
        self.category_form_color = category.get("color_bg", "bg-gray-100")
        self.is_category_dialog_open = True

    @rx.event
    def set_category_dialog_open(self, value: bool):
        self.is_category_dialog_open = value

    @rx.event
    def set_category_form_name(self, val: str):
        self.category_form_name = val
        if self.editing_category_id == 0:
            self.category_form_slug = val.lower().replace(" ", "-")

    @rx.event
    def set_category_form_slug(self, val: str):
        self.category_form_slug = val

    @rx.event
    def set_category_form_icon(self, val: str):
        self.category_form_icon = val

    @rx.event
    def set_category_form_color(self, val: str):
        self.category_form_color = val

    @rx.event
    async def save_category(self):
        db = DatabaseManager()
        category_data = {
            "name": self.category_form_name,
            "slug": self.category_form_slug,
            "icon": self.category_form_icon,
            "color_bg": self.category_form_color,
            "is_active": True,
        }
        if self.editing_category_id == 0:
            if db.supabase:
                await db.create_category(category_data)
            else:
                new_id = len(data.CATEGORIES) + 1
                category_data["id"] = new_id
                data.CATEGORIES.append(category_data)
        elif db.supabase:
            await db.update_category(self.editing_category_id, category_data)
        else:
            for cat in data.CATEGORIES:
                if cat["id"] == self.editing_category_id:
                    cat.update(category_data)
                    break
        self.is_category_dialog_open = False
        await self.fetch_data()
        return rx.toast("Category saved successfully")

    @rx.event
    async def toggle_category_status(self, category_id: int):
        db = DatabaseManager()
        if db.supabase:
            current_status = True
            for c in self.categories:
                if c["id"] == category_id:
                    current_status = c.get("is_active", True)
                    break
            await db.update_category(category_id, {"is_active": not current_status})
            await self.fetch_data()
            return rx.toast(
                f"Category {('deactivated' if current_status else 'activated')}"
            )

    @rx.event
    async def delete_category(self, category_id: int):
        db = DatabaseManager()
        if db.supabase:
            await db.delete_category(category_id)
        else:
            data.CATEGORIES = [c for c in data.CATEGORIES if c["id"] != category_id]
        await self.fetch_data()
        return rx.toast("Category deleted")