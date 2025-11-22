import reflex as rx
from app.data import ProductDict, OrderDict, WeeklyStatDict, PayoutDict
import app.data as data
from app.utils.database import DatabaseManager
import logging


class ShopOwnerState(rx.State):
    shop_id: int = 1
    shop_name: str = "Fresh Mart Grocery"
    products: list[ProductDict] = []
    orders: list[OrderDict] = []
    weekly_stats: list[WeeklyStatDict] = [
        {"day": "Mon", "revenue": 1200, "orders": 12},
        {"day": "Tue", "revenue": 1500, "orders": 15},
        {"day": "Wed", "revenue": 1100, "orders": 10},
        {"day": "Thu", "revenue": 1800, "orders": 18},
        {"day": "Fri", "revenue": 2200, "orders": 22},
        {"day": "Sat", "revenue": 2800, "orders": 25},
        {"day": "Sun", "revenue": 2500, "orders": 20},
    ]
    payouts: list[PayoutDict] = []
    is_product_dialog_open: bool = False
    editing_product_id: int = 0
    form_name: str = ""
    form_price: str = ""
    form_unit: str = ""
    form_image_url: str = ""
    form_description: str = ""

    @rx.event
    async def on_mount(self):
        await self.fetch_data()

    @rx.event
    async def fetch_data(self):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if auth_state.current_user and auth_state.current_user.get("shop_id"):
            self.shop_id = auth_state.current_user["shop_id"]
        db = DatabaseManager()
        if db.supabase:
            shops = await db.get_shops()
            shop = next((s for s in shops if s["id"] == self.shop_id), None)
            if shop:
                self.shop_name = shop["name"]
            self.products = await db.get_products(self.shop_id)
            db_orders = await db.get_orders_by_shop(self.shop_id)
            processed_orders = []
            for o in db_orders:
                o["items"] = o.pop("order_items", [])
                processed_orders.append(o)
            self.orders = processed_orders
        else:
            shops = data.SHOPS
            shop = next((s for s in shops if s["id"] == self.shop_id), None)
            if shop:
                self.shop_name = shop["name"]
            self.products = [p for p in data.PRODUCTS if p["shop_id"] == self.shop_id]
            self.orders = [o for o in data.ORDERS if o.get("shop_id") == self.shop_id]
        self.generate_payouts()

    @rx.event
    def generate_payouts(self):
        self.payouts = []
        for order in self.orders:
            if order["status"] in ["Delivered", "Completed"]:
                commission = order["subtotal"] * 0.1
                self.payouts.append(
                    {
                        "id": f"PAY-{order['id']}",
                        "date": order["date"],
                        "order_id": order["id"],
                        "order_amount": order["subtotal"],
                        "commission": commission,
                        "payout_amount": order["subtotal"] - commission,
                        "status": "Processed",
                    }
                )

    @rx.var
    def total_orders_today(self) -> int:
        return 12

    @rx.var
    def total_revenue_today(self) -> float:
        return 4500.0

    @rx.var
    def pending_orders(self) -> list[OrderDict]:
        return [o for o in self.orders if o["status"] == "Pending"]

    @rx.var
    def active_orders(self) -> list[OrderDict]:
        return [
            o
            for o in self.orders
            if o["status"] in ["Confirmed", "Packed", "Ready", "Out for Delivery"]
        ]

    @rx.var
    def completed_orders(self) -> list[OrderDict]:
        return [o for o in self.orders if o["status"] in ["Delivered", "Completed"]]

    @rx.var
    def total_earnings(self) -> float:
        return sum((p["payout_amount"] for p in self.payouts))

    @rx.event
    def open_add_product_dialog(self):
        self.editing_product_id = 0
        self.form_name = ""
        self.form_price = ""
        self.form_unit = ""
        self.form_image_url = ""
        self.form_description = ""
        self.is_product_dialog_open = True

    @rx.event
    def open_edit_product_dialog(self, product: ProductDict):
        self.editing_product_id = product["id"]
        self.form_name = product["name"]
        self.form_price = str(product["price"])
        self.form_unit = product["unit"]
        self.form_image_url = product["image_url"]
        self.form_description = product["description"]
        self.is_product_dialog_open = True

    @rx.event
    def close_product_dialog(self):
        self.is_product_dialog_open = False

    @rx.event
    def set_product_dialog_open(self, value: bool):
        self.is_product_dialog_open = value

    @rx.event
    async def save_product(self):
        try:
            price = float(self.form_price)
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return rx.window_alert("Invalid price")
        db = DatabaseManager()
        if self.editing_product_id == 0:
            new_product = {
                "shop_id": self.shop_id,
                "name": self.form_name,
                "price": price,
                "original_price": price * 1.1,
                "image_url": self.form_image_url
                or "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=200&q=80",
                "description": self.form_description,
                "is_available": True,
                "unit": self.form_unit,
            }
            await db.create_product(new_product)
        else:
            updates = {
                "name": self.form_name,
                "price": price,
                "unit": self.form_unit,
                "image_url": self.form_image_url,
                "description": self.form_description,
            }
            await db.update_product(self.editing_product_id, updates)
        self.is_product_dialog_open = False
        await self.fetch_data()
        return rx.toast(
            "Product saved successfully"
            if self.editing_product_id == 0
            else "Product updated"
        )

    @rx.event
    async def toggle_stock(self, product_id: int):
        db = DatabaseManager()
        current_status = True
        for p in self.products:
            if p["id"] == product_id:
                current_status = p["is_available"]
                break
        await db.toggle_product_stock(product_id, not current_status)
        await self.fetch_data()

    @rx.event
    async def update_order_status(self, order_id: str, status: str):
        db = DatabaseManager()
        await db.update_order_status(order_id, status)
        await self.fetch_data()

    @rx.event
    def set_form_name(self, value: str):
        self.form_name = value

    @rx.event
    def set_form_price(self, value: str):
        self.form_price = value

    @rx.event
    def set_form_unit(self, value: str):
        self.form_unit = value

    @rx.event
    def set_form_image_url(self, value: str):
        self.form_image_url = value

    @rx.event
    def set_form_description(self, value: str):
        self.form_description = value