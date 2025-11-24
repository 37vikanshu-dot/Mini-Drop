import reflex as rx
from app.data import OrderDict, RiderDict
import app.data as data
from app.utils.database import DatabaseManager
from app.states.auth_state import AuthState
import logging


class RiderState(rx.State):
    rider: dict = {}
    available_orders: list[OrderDict] = []
    assigned_orders: list[OrderDict] = []
    completed_orders_history: list[OrderDict] = []
    today_earnings: float = 0.0
    today_orders_count: int = 0

    @rx.var
    def rider_id(self) -> str:
        if self.rider and "id" in self.rider:
            return self.rider["id"]
        return ""

    @rx.var
    def is_online(self) -> bool:
        return self.rider.get("status") == "Online"

    @rx.event
    async def on_mount(self):
        await self.fetch_rider_profile()
        await self.fetch_orders()

    @rx.event
    async def fetch_rider_profile(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            self.rider = {}
            return
        user_id = auth_state.current_user.get("id", "")
        rider_id = ""
        if user_id.startswith("rider_"):
            rider_id = user_id.replace("rider_", "")
        if not rider_id:
            return
        db = DatabaseManager()
        if db.supabase:
            rider_data = await db.get_rider_by_id(rider_id)
            if rider_data:
                self.rider = rider_data
                self.today_earnings = rider_data.get("earnings", 0.0)
                self.today_orders_count = rider_data.get("completed_orders", 0)
            else:
                logging.warning(f"Rider profile not found for ID: {rider_id}")
                self.rider = {}
        else:
            self.rider = next((r for r in data.RIDERS if r["id"] == rider_id), {})

    @rx.event
    async def fetch_orders(self):
        db = DatabaseManager()
        if db.supabase:
            self.available_orders = await db.get_available_orders()
            if self.rider_id:
                all_my_orders = await db.get_rider_orders(self.rider_id)
                self.assigned_orders = [
                    o for o in all_my_orders if o["status"] == "Out for Delivery"
                ]
                self.completed_orders_history = [
                    o
                    for o in all_my_orders
                    if o["status"] in ["Delivered", "Completed"]
                ]
        else:
            self.available_orders = [o for o in data.ORDERS if o["status"] == "Ready"]
            self.assigned_orders = []
            self.completed_orders_history = []

    @rx.event
    async def toggle_status(self):
        new_status = "Offline" if self.is_online else "Online"
        db = DatabaseManager()
        if self.rider_id and db.supabase:
            success = await db.toggle_rider_status(self.rider_id, new_status)
            if success:
                self.rider["status"] = new_status
                rx.toast(f"You are now {new_status}")
            else:
                rx.toast.error("Failed to update status")
        else:
            self.rider["status"] = new_status

    @rx.event
    async def accept_order(self, order_id: str):
        if not self.is_online:
            return rx.window_alert("Please go online to accept orders")
        db = DatabaseManager()
        if self.rider_id and db.supabase:
            success = await db.assign_order_to_rider(order_id, self.rider_id)
            if success:
                rx.toast("Order accepted! 🚀")
                await self.fetch_orders()
                return rx.redirect("/rider/deliveries")
            else:
                rx.toast.error("Failed to accept order")
        else:
            rx.toast("Demo: Order accepted")

    @rx.event
    async def mark_delivered(self, order_id: str):
        db = DatabaseManager()
        if db.supabase:
            success = await db.update_order_status(order_id, "Delivered")
            if success:
                earnings = 40.0
                await db.update_rider_earnings(self.rider_id, earnings)
                rx.toast(f"Order delivered! Earned ₹{earnings}")
                await self.fetch_orders()
                await self.fetch_rider_profile()
            else:
                rx.toast.error("Failed to update status")
        else:
            rx.toast("Demo: Order delivered")