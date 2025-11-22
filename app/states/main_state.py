import reflex as rx
from app.data import (
    ShopDict,
    ProductDict,
    CategoryDict,
    SavedAddressDict,
    OrderDict,
    OrderItemDict,
)
import app.data as data
from app.states.auth_state import AuthState
from app.utils.database import DatabaseManager
import datetime
import logging
import random


class AppState(rx.State):
    categories: list[CategoryDict] = []
    shops: list[ShopDict] = []
    products: list[ProductDict] = []
    search_query: str = ""
    active_category_filter: str = "all"
    current_shop_id: int = 0
    cart: dict[str, int] = {}
    is_cart_open: bool = False
    _user_name_default: str = "Guest User"
    user_phone: str = ""
    user_email: str = "guest@example.com"
    checkout_address: str = ""
    checkout_payment_method: str = "UPI"
    saved_addresses: list[SavedAddressDict] = []
    orders: list[OrderDict] = []

    @rx.event
    async def on_mount(self):
        """Fetch initial data from database or mock data."""
        db = DatabaseManager()
        if db.supabase:
            self.categories = await db.get_categories()
            self.shops = await db.get_shops()
            self.products = await db.get_products()
        else:
            self.categories = data.CATEGORIES
            self.shops = data.SHOPS
            self.products = data.PRODUCTS
        auth_state = await self.get_state(AuthState)
        if auth_state.is_authenticated and auth_state.user_id_cookie:
            if db.supabase:
                db_orders = await db.get_orders_by_user(auth_state.user_id_cookie)
                processed_orders = []
                for o in db_orders:
                    o["items"] = o.pop("order_items", [])
                    processed_orders.append(o)
                self.orders = processed_orders
            else:
                pass

    @rx.var
    async def user_name(self) -> str:
        auth_state = await self.get_state(AuthState)
        if auth_state.current_user:
            return auth_state.current_user["name"]
        return self._user_name_default

    @rx.var
    def cart_items_details(self) -> list[OrderItemDict]:
        items = []
        for pid_str, qty in self.cart.items():
            for p in self.products:
                if str(p["id"]) == pid_str:
                    items.append(
                        {
                            "product_id": p["id"],
                            "name": p["name"],
                            "price": p["price"],
                            "quantity": qty,
                            "image_url": p["image_url"],
                        }
                    )
        return items

    @rx.var
    def delivery_fee(self) -> float:
        return 15.0 if self.cart_total > 0 else 0.0

    @rx.var
    def cart_grand_total(self) -> float:
        return self.cart_total + self.delivery_fee

    @rx.var
    def active_order(self) -> OrderDict | None:
        order_id = self.router.page.params.get("id")
        if not order_id:
            return None
        for order in self.orders:
            if str(order["id"]) == order_id:
                return order
        return None

    @rx.event
    def set_checkout_address(self, address: str):
        self.checkout_address = address

    @rx.event
    def set_payment_method(self, method: str):
        self.checkout_payment_method = method

    @rx.event
    async def place_order(self):
        if not self.checkout_address:
            return rx.window_alert("Please enter a delivery address.")
        auth_state = await self.get_state(AuthState)
        user_id = auth_state.user_id_cookie if auth_state.user_id_cookie else "guest"
        shop_items = {}
        for item in self.cart_items_details:
            prod = next(
                (p for p in self.products if p["id"] == item["product_id"]), None
            )
            if prod:
                sid = prod["shop_id"]
                if sid not in shop_items:
                    shop_items[sid] = []
                shop_items[sid].append(item)
        created_order_ids = []
        db = DatabaseManager()
        for shop_id, items in shop_items.items():
            subtotal = sum((i["price"] * i["quantity"] for i in items))
            delivery = 15.0
            total = subtotal + delivery
            now = datetime.datetime.now()
            order_id = f"ORD-{random.randint(10000, 99999)}"
            order_data = {
                "id": order_id,
                "subtotal": subtotal,
                "delivery_fee": delivery,
                "total_amount": total,
                "status": "Confirmed",
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M"),
                "delivery_address": self.checkout_address,
                "payment_method": self.checkout_payment_method,
                "shop_id": shop_id,
                "user_id": user_id,
            }
            created_order = await db.create_order(order_data)
            if created_order:
                order_items_data = []
                for i in items:
                    order_items_data.append(
                        {
                            "order_id": order_id,
                            "product_id": i["product_id"],
                            "name": i["name"],
                            "price": i["price"],
                            "quantity": i["quantity"],
                            "image_url": i["image_url"],
                        }
                    )
                await db.create_order_items(order_items_data)
                new_order_full = order_data.copy()
                new_order_full["items"] = items
                self.orders.insert(0, new_order_full)
                created_order_ids.append(order_id)
            else:
                data.ORDERS.append(order_data)
                created_order_ids.append(order_id)
        self.cart = {}
        if created_order_ids:
            return rx.redirect(f"/tracking/{created_order_ids[0]}")
        return rx.redirect("/")

    @rx.event
    def update_profile(self, form_data: dict):
        self._user_name_default = form_data.get("name", self._user_name_default)
        self.user_email = form_data.get("email", self.user_email)
        self.user_phone = form_data.get("phone", self.user_phone)
        return rx.toast("Profile updated successfully!")

    @rx.var
    def filtered_shops(self) -> list[ShopDict]:
        if self.active_category_filter == "all":
            return self.shops
        return [
            shop
            for shop in self.shops
            if shop["category_slug"] == self.active_category_filter
        ]

    @rx.var
    def featured_shops(self) -> list[ShopDict]:
        return [shop for shop in self.shops if shop["is_featured"]]

    @rx.var
    def quick_items(self) -> list[ProductDict]:
        return self.products[:5]

    @rx.var
    def current_shop(self) -> ShopDict | None:
        if self.current_shop_id == 0:
            return None
        for shop in self.shops:
            if shop["id"] == self.current_shop_id:
                return shop
        return None

    @rx.var
    def shop_products(self) -> list[ProductDict]:
        if self.current_shop_id == 0:
            return []
        return [p for p in self.products if p["shop_id"] == self.current_shop_id]

    @rx.var
    def cart_count(self) -> int:
        return sum(self.cart.values())

    @rx.var
    def cart_total(self) -> float:
        total = 0.0
        for pid, qty in self.cart.items():
            for p in self.products:
                if p["id"] == int(pid):
                    total += p["price"] * qty
        return total

    @rx.event
    def set_category_filter(self, category_slug: str):
        self.active_category_filter = category_slug

    @rx.event
    def select_shop(self, shop_id: int):
        self.current_shop_id = shop_id

    @rx.event
    def update_search(self, query: str):
        self.search_query = query

    @rx.event
    def add_to_cart(self, product_id: int):
        pid_str = str(product_id)
        current_qty = self.cart.get(pid_str, 0)
        self.cart[pid_str] = current_qty + 1

    @rx.event
    def remove_from_cart(self, product_id: int):
        pid_str = str(product_id)
        current_qty = self.cart.get(pid_str, 0)
        if current_qty > 1:
            self.cart[pid_str] = current_qty - 1
        elif current_qty == 1:
            del self.cart[pid_str]

    @rx.event
    def get_product_quantity(self, product_id: int) -> int:
        return self.cart.get(product_id, 0)

    @rx.event
    def use_saved_address(self, address: str):
        self.checkout_address = address

    @rx.event
    async def load_shop_page(self):
        """Load shop details based on URL parameter."""
        shop_id_param = self.router.page.params.get("id")
        if shop_id_param:
            try:
                self.current_shop_id = int(shop_id_param)
            except ValueError:
                logging.exception(f"Invalid shop ID: {shop_id_param}")
                self.current_shop_id = 0
        if not self.shops or not self.products:
            await self.on_mount()