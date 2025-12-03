import reflex as rx
from app.components.layout import layout
from app.states.main_state import AppState
from app.states.payment_state import PaymentState

RAZORPAY_SCRIPT = """
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script>
function handlePayment(orderId, amount, keyId) {
    var options = {
        "key": keyId,
        "amount": amount * 100,
        "currency": "INR",
        "name": "Mini Drop",
        "description": "Hyperlocal Delivery",
        "image": "https://api.dicebear.com/9.x/notionists/svg?seed=MiniDrop",
        "order_id": orderId,
        "handler": function (response){
            // Call backend verification
            // We trigger the event handler defined in PaymentState
            reflex.sendEvent("app.states.payment_state.PaymentState.verify_payment", 
                {payment_id: response.razorpay_payment_id, 
                 order_id: response.razorpay_order_id, 
                 signature: response.razorpay_signature}
            );
        },
        "prefill": {
            "name": "Mini Drop User",
            "email": "user@minidrop.com",
            "contact": "9999999999"
        },
        "theme": {
            "color": "#6200EA"
        },
        "modal": {
            "ondismiss": function(){
                reflex.sendEvent("app.states.payment_state.PaymentState.payment_failed");
            }
        }
    };
    var rzp1 = new Razorpay(options);
    rzp1.open();

    rzp1.on('payment.failed', function (response){
        reflex.sendEvent("app.states.payment_state.PaymentState.payment_failed");
    });
}
</script>
"""


def address_card(address: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                rx.cond(address["type"] == "Home", "home", "briefcase"),
                class_name="w-5 h-5 text-[#6200EA]",
            ),
            rx.el.div(
                rx.el.h4(address["type"], class_name="text-sm font-bold text-gray-900"),
                rx.el.p(address["address"], class_name="text-xs text-gray-500 mt-0.5"),
                class_name="ml-3 flex-1",
            ),
            rx.el.button(
                "Select",
                on_click=AppState.use_saved_address(address["address"]),
                class_name="text-xs font-bold text-[#6200EA] bg-purple-50 px-3 py-1.5 rounded-lg hover:bg-purple-100",
            ),
            class_name="flex items-center p-3",
        ),
        class_name="bg-white rounded-xl border border-gray-100 shadow-sm mb-3",
    )


def checkout_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.h1("Checkout", class_name="text-2xl font-bold text-gray-900 mb-6"),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Delivery Address",
                        class_name="text-sm font-bold text-gray-900 mb-4",
                    ),
                    rx.el.textarea(
                        placeholder="Enter your full delivery address...",
                        on_change=AppState.set_checkout_address,
                        class_name="w-full bg-white border border-gray-200 rounded-xl p-3 text-sm focus:ring-2 focus:ring-[#6200EA] focus:border-transparent min-h-[100px] mb-4",
                        default_value=AppState.checkout_address,
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "Saved Addresses",
                            class_name="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3",
                        ),
                        rx.foreach(AppState.saved_addresses, address_card),
                        class_name="mb-6",
                    ),
                ),
                rx.el.div(
                    rx.el.h3(
                        "Payment Method",
                        class_name="text-sm font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="payment",
                                checked=AppState.checkout_payment_method == "UPI",
                                on_change=lambda: AppState.set_payment_method("UPI"),
                                class_name="w-4 h-4 text-[#6200EA] focus:ring-[#6200EA]",
                            ),
                            rx.el.span(
                                "UPI (Google Pay / PhonePe)",
                                class_name="ml-3 text-sm font-medium text-gray-900",
                            ),
                            class_name="flex items-center p-4 border border-gray-200 rounded-xl mb-3 cursor-pointer bg-white",
                        ),
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="payment",
                                checked=AppState.checkout_payment_method == "COD",
                                on_change=lambda: AppState.set_payment_method("COD"),
                                class_name="w-4 h-4 text-[#6200EA] focus:ring-[#6200EA]",
                            ),
                            rx.el.span(
                                "Cash on Delivery",
                                class_name="ml-3 text-sm font-medium text-gray-900",
                            ),
                            class_name="flex items-center p-4 border border-gray-200 rounded-xl cursor-pointer bg-white",
                        ),
                        class_name="mb-8",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Order Summary",
                            class_name="text-sm font-bold text-gray-900 mb-4",
                        ),
                        rx.cond(
                            AppState.applied_coupon,
                            rx.el.div(
                                rx.el.span(
                                    "Discount Applied",
                                    class_name="text-sm text-green-600",
                                ),
                                rx.el.span(
                                    f"-₹{AppState.coupon_discount_amount}",
                                    class_name="text-sm font-bold text-green-600",
                                ),
                                class_name="flex justify-between items-center mb-2",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Total Amount", class_name="text-base text-gray-600"
                            ),
                            rx.el.span(
                                f"₹{AppState.cart_grand_total}",
                                class_name="text-xl font-bold text-[#6200EA]",
                            ),
                            class_name="flex justify-between items-center",
                        ),
                        class_name="bg-gray-50 rounded-xl p-4 mb-6",
                    ),
                    rx.cond(
                        AppState.checkout_payment_method == "UPI",
                        rx.el.button(
                            rx.cond(
                                PaymentState.is_processing,
                                rx.spinner(size="1", class_name="mr-2"),
                                rx.icon("credit-card", class_name="w-5 h-5 mr-2"),
                            ),
                            rx.cond(
                                PaymentState.is_processing,
                                "Processing Payment...",
                                "Pay Now",
                            ),
                            on_click=PaymentState.create_razorpay_order,
                            disabled=PaymentState.is_processing,
                            class_name="flex items-center justify-center w-full bg-[#6200EA] text-white py-3.5 rounded-xl font-bold shadow-lg hover:shadow-xl hover:bg-[#5000CA] transition-all active:scale-95",
                        ),
                        rx.el.button(
                            "Place COD Order",
                            on_click=AppState.place_order,
                            class_name="w-full bg-gray-900 text-white py-3.5 rounded-xl font-bold shadow-lg hover:shadow-xl hover:bg-gray-800 transition-all active:scale-95",
                        ),
                    ),
                    rx.el.div(rx.html(RAZORPAY_SCRIPT)),
                ),
                class_name="max-w-2xl mx-auto",
            ),
            class_name="max-w-2xl mx-auto px-4",
        )
    )