import reflex as rx
from app.components.layout import layout
from app.states.main_state import AppState
from app.data import OrderDict


def order_card(order: OrderDict) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h4(order["id"], class_name="text-sm font-bold text-gray-900"),
                    rx.el.p(
                        f"{order['date']} at {order['time']}",
                        class_name="text-xs text-gray-500",
                    ),
                ),
                rx.el.span(
                    order["status"],
                    class_name="text-xs font-bold px-2 py-1 bg-green-100 text-green-700 rounded-full",
                ),
                class_name="flex justify-between items-start mb-3",
            ),
            rx.el.div(
                rx.el.span(
                    f"{order['items'].length()} Items",
                    class_name="text-xs text-gray-600",
                ),
                rx.el.span(
                    f"Total: ₹{order['total_amount']}",
                    class_name="text-sm font-bold text-gray-900",
                ),
                class_name="flex justify-between items-center pt-3 border-t border-gray-50",
            ),
            class_name="bg-white p-4 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all mb-3",
        ),
        href=f"/tracking/{order['id']}",
    )


def account_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src="https://api.dicebear.com/9.x/notionists/svg?seed=Felix",
                        class_name="w-20 h-20 rounded-full bg-gray-100 border-4 border-white shadow-md",
                    ),
                    rx.el.div(
                        rx.el.h1(
                            AppState.user_name,
                            class_name="text-xl font-bold text-gray-900",
                        ),
                        rx.el.p(
                            AppState.user_email, class_name="text-sm text-gray-500"
                        ),
                        class_name="ml-4",
                    ),
                    class_name="flex items-center mb-8",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Membership", class_name="text-sm font-bold text-gray-900 mb-3"
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h4(
                                "Pro Member",
                                class_name="text-lg font-bold text-white mb-1",
                            ),
                            rx.el.p(
                                "Free delivery on all orders",
                                class_name="text-white/90 text-xs",
                            ),
                        ),
                        rx.el.button(
                            "Renew",
                            class_name="bg-white text-[#6200EA] px-4 py-1.5 rounded-full text-xs font-bold",
                        ),
                        class_name="bg-gradient-to-r from-[#6200EA] to-[#9046FC] p-5 rounded-2xl shadow-lg shadow-purple-200 flex justify-between items-center mb-8",
                    ),
                ),
                rx.el.div(
                    rx.el.h3(
                        "Recent Orders",
                        class_name="text-sm font-bold text-gray-900 mb-4",
                    ),
                    rx.cond(
                        AppState.orders.length() > 0,
                        rx.foreach(AppState.orders, order_card),
                        rx.el.div(
                            rx.el.p(
                                "No orders yet",
                                class_name="text-sm text-gray-500 text-center py-8",
                            )
                        ),
                    ),
                ),
                class_name="max-w-2xl mx-auto",
            ),
            class_name="max-w-2xl mx-auto px-4",
        )
    )