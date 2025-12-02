import reflex as rx
import os
import json
from typing import Optional, Any
from google import genai
from pydantic import BaseModel
from app.states.main_state import AppState
from app.states.auth_state import AuthState
from app.data import ProductDict
from app.utils.database import DatabaseManager
import logging


class ProductRecommendation(BaseModel):
    product_id: int
    quantity: int
    reason: str


class SmartBasketResponse(BaseModel):
    recommendations: list[ProductRecommendation]
    theme: str
    total_estimated_value: float


class AdminInsightData(BaseModel):
    demand_prediction: str
    top_selling_analysis: str
    stock_risks: list[str]
    peak_hour_analysis: str
    user_buying_patterns: str


class GenieItemDict(ProductDict):
    quantity: int
    reason: str


class AIState(rx.State):
    smart_basket: list[GenieItemDict] = []
    smart_basket_theme: str = ""
    genie_recommendations: list[GenieItemDict] = []
    genie_input: str = ""
    is_genie_open: bool = False
    is_loading_genie: bool = False
    is_loading_basket: bool = False
    admin_insights: Optional[AdminInsightData] = None
    is_loading_insights: bool = False
    error_message: str = ""

    def _get_client(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            self.error_message = "Google API Key is missing."
            return None
        return genai.Client(api_key=api_key)

    async def _get_product_context(self) -> str:
        main_state = await self.get_state(AppState)
        products = main_state.products
        context = """Available Products Catalog:
"""
        for p in products:
            context += f"ID: {p['id']}, Name: {p['name']}, Price: {p['price']}, Unit: {p['unit']}\n"
        return context

    @rx.event
    def set_genie_input(self, val: str):
        self.genie_input = val

    @rx.event
    def handle_key_down(self, key: str):
        if key == "Enter":
            return AIState.ask_genie

    @rx.event
    def toggle_genie_modal(self):
        self.is_genie_open = not self.is_genie_open
        if not self.is_genie_open:
            self.genie_recommendations = []
            self.genie_input = ""

    @rx.event
    async def generate_smart_basket(self):
        self.is_loading_basket = True
        self.error_message = ""
        client = self._get_client()
        if not client:
            self.is_loading_basket = False
            return
        try:
            product_ctx = await self._get_product_context()
            auth_state = await self.get_state(AuthState)
            main_state = await self.get_state(AppState)
            user_orders_context = "User has no previous orders."
            if auth_state.current_user:
                user_id = auth_state.current_user["id"]
                user_orders = [
                    o for o in main_state.orders if o.get("user_id") == user_id
                ]
                if user_orders:
                    user_orders_context = f"User Order History (last {min(len(user_orders), 5)} orders):\n"
                    for o in user_orders[:5]:
                        items_str = ", ".join(
                            [
                                f"{i['quantity']}x {i['name']}"
                                for i in o.get("items", [])
                            ]
                        )
                        user_orders_context += (
                            f"- Date: {o['date']}, Items: {items_str}\n"
                        )
            prompt = f"\n            {product_ctx}\n\n            {user_orders_context}\n\n            Based on the user's order history (or general popularity if no history), create a personalized weekly shopping basket.\n            Recommend 4-6 essential items. Return the product_id exactly as listed in the catalog.\n            "
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SmartBasketResponse,
                ),
            )
            parsed_response = response.parsed
            self.smart_basket = []
            self.smart_basket_theme = parsed_response.theme
            for rec in parsed_response.recommendations:
                product = next(
                    (p for p in main_state.products if p["id"] == rec.product_id), None
                )
                if product:
                    self.smart_basket.append(
                        {**product, "quantity": rec.quantity, "reason": rec.reason}
                    )
        except Exception as e:
            logging.exception(f"Smart Basket Error: {e}")
            self.error_message = "Failed to generate smart basket. Please try again."
        finally:
            self.is_loading_basket = False

    @rx.event
    async def add_smart_basket_to_cart(self):
        main_state = await self.get_state(AppState)
        count = 0
        for item in self.smart_basket:
            pid = str(item["id"])
            qty = item["quantity"]
            current_qty = main_state.cart.get(pid, 0)
            main_state.cart[pid] = current_qty + qty
            count += qty
        rx.toast(f"Added {count} items to your cart!")

    @rx.event
    async def ask_genie(self):
        if not self.genie_input.strip():
            return
        self.is_loading_genie = True
        self.is_genie_open = True
        self.error_message = ""
        client = self._get_client()
        if not client:
            self.is_loading_genie = False
            return
        try:
            product_ctx = await self._get_product_context()
            prompt = f'''\n            {product_ctx}\n\n            User Request: "{self.genie_input}"\n\n            Interpret the user's request and recommend products from the catalog.\n            If they ask for a meal (e.g., "breakfast"), suggest ingredients.\n            If they ask for a party, suggest snacks/drinks.\n            Return product_ids exactly as in the catalog.\n            '''
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=list[ProductRecommendation],
                ),
            )
            recs = response.parsed
            main_state = await self.get_state(AppState)
            self.genie_recommendations = []
            for rec in recs:
                product = next(
                    (p for p in main_state.products if p["id"] == rec.product_id), None
                )
                if product:
                    self.genie_recommendations.append(
                        {**product, "quantity": rec.quantity, "reason": rec.reason}
                    )
        except Exception as e:
            logging.exception(f"Genie Error: {e}")
            self.error_message = "Genie is having trouble thinking right now."
        finally:
            self.is_loading_genie = False

    @rx.event
    async def add_genie_item_to_cart(self, product_id: int, quantity: int):
        main_state = await self.get_state(AppState)
        pid = str(product_id)
        current_qty = main_state.cart.get(pid, 0)
        main_state.cart[pid] = current_qty + quantity
        rx.toast("Item added to cart")

    @rx.event
    async def generate_admin_insights(self):
        self.is_loading_insights = True
        self.error_message = ""
        client = self._get_client()
        if not client:
            self.is_loading_insights = False
            return
        try:
            from app.states.admin_state import AdminState

            admin_state = await self.get_state(AdminState)
            orders_summary = """Recent Orders:
"""
            for o in admin_state.orders[:20]:
                orders_summary += f"- Time: {o['time']}, Amount: {o['total_amount']}, Items: {len(o.get('items', []))}\n"
            shops_summary = f"Total Shops: {len(admin_state.shops)}\n"
            riders_summary = f"Total Riders: {len(admin_state.riders)}\n"
            prompt = f"\n            Analyze the following hyperlocal delivery platform data:\n            {shops_summary}\n            {riders_summary}\n            {orders_summary}\n\n            Provide strategic insights for the admin.\n            1. Predict demand trends.\n            2. Analyze top selling categories/items (infer from context).\n            3. Identify potential stock or operational risks.\n            4. Analyze peak hours based on order times.\n            5. Summarize user buying patterns.\n            "
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AdminInsightData,
                ),
            )
            self.admin_insights = response.parsed
        except Exception as e:
            logging.exception(f"Admin Insights Error: {e}")
            self.error_message = "Failed to generate insights."
        finally:
            self.is_loading_insights = False