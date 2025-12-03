import reflex as rx
import logging
import os
import time

try:
    import razorpay
except ImportError as e:
    razorpay = None
    logging.exception(
        f"Razorpay not installed. Install it with 'pip install razorpay'. Error: {e}"
    )
from app.states.main_state import AppState


class PaymentState(rx.State):
    razorpay_order_id: str = ""
    payment_status: str = "pending"
    is_processing: bool = False

    @rx.event
    async def create_razorpay_order(self):
        """Create a Razorpay order for the current cart."""
        if not razorpay:
            return rx.toast.error(
                "Payment gateway not configured (Razorpay library missing)"
            )
        main_state = await self.get_state(AppState)
        if main_state.cart_total <= 0:
            return rx.toast.error("Cart is empty")
        if not main_state.checkout_address:
            return rx.window_alert("Please enter a delivery address")
        key_id = os.environ.get("RAZORPAY_KEY_ID")
        key_secret = os.environ.get("RAZORPAY_KEY_SECRET")
        if not key_id or not key_secret:
            self.razorpay_order_id = f"order_mock_{int(time.time())}"
            return rx.call_script(
                f"handlePayment('{self.razorpay_order_id}', {main_state.cart_grand_total}, '{key_id or 'test_key'}')"
            )
        try:
            self.is_processing = True
            client = razorpay.Client(auth=(key_id, key_secret))
            amount_in_paise = int(main_state.cart_grand_total * 100)
            order_data = {
                "amount": amount_in_paise,
                "currency": "INR",
                "receipt": f"rcpt_{int(time.time())}",
                "payment_capture": 1,
            }
            order = client.order.create(data=order_data)
            self.razorpay_order_id = order["id"]
            return rx.call_script(
                f"handlePayment('{self.razorpay_order_id}', {main_state.cart_grand_total}, '{key_id}')"
            )
        except Exception as e:
            logging.exception(f"Razorpay order creation failed: {e}")
            self.is_processing = False
            return rx.toast.error("Failed to initiate payment")

    @rx.event
    async def verify_payment(self, payment_id: str, order_id: str, signature: str):
        """Verify the payment signature from Razorpay."""
        key_secret = os.environ.get("RAZORPAY_KEY_SECRET")
        verified = False
        if not key_secret:
            verified = True
        elif razorpay:
            try:
                client = razorpay.Client(
                    auth=(os.environ.get("RAZORPAY_KEY_ID"), key_secret)
                )
                client.utility.verify_payment_signature(
                    {
                        "razorpay_order_id": order_id,
                        "razorpay_payment_id": payment_id,
                        "razorpay_signature": signature,
                    }
                )
                verified = True
            except Exception as e:
                logging.exception(f"Payment verification failed: {e}")
                verified = False
        if verified:
            self.payment_status = "success"
            self.is_processing = False
            main_state = await self.get_state(AppState)
            return await main_state.place_order()
        else:
            self.payment_status = "failed"
            self.is_processing = False
            return rx.toast.error("Payment verification failed")

    @rx.event
    def payment_failed(self):
        self.is_processing = False
        return rx.toast.error("Payment failed or cancelled")