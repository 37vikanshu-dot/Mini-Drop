import reflex as rx
from app.components.rider_layout import rider_layout
from app.states.rider_state import RiderState
from app.components.protected_route import protected_rider
from app.data import OrderDict


def available_order_card(order: OrderDict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h4(f"#{order['id']}", class_name="font-bold text-gray-900"),
                rx.el.span(
                    "Ready for Pickup",
                    class_name="text-xs font-bold px-2 py-1 bg-blue-100 text-blue-700 rounded-full",
                ),
                class_name="flex justify-between items-center mb-2",
            ),
            rx.el.div(
                rx.el.p(
                    order["delivery_address"],
                    class_name="text-sm text-gray-600 mb-3 line-clamp-2",
                ),
                rx.el.div(
                    rx.el.span(
                        f"₹{order['total_amount']}",
                        class_name="font-bold text-gray-900",
                    ),
                    rx.el.span(" • ", class_name="text-gray-400"),
                    rx.el.span(
                        f"{order['items'].length()} Items",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex items-center mb-4",
                ),
                rx.el.button(
                    "Accept Order",
                    on_click=RiderState.accept_order(order["id"]),
                    class_name="w-full bg-[#6200EA] text-white py-2 rounded-lg font-bold hover:bg-[#5000CA] transition-colors",
                ),
            ),
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all",
    )


def orders_page() -> rx.Component:
    return protected_rider(
        rider_layout(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Available Orders",
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("refresh-cw", class_name="w-4 h-4 mr-2"),
                        "Refresh",
                        on_click=RiderState.fetch_orders,
                        class_name="flex items-center text-sm font-bold text-[#6200EA] hover:bg-purple-50 px-3 py-1.5 rounded-lg transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.cond(
                    RiderState.available_orders.length() > 0,
                    rx.el.div(
                        rx.foreach(RiderState.available_orders, available_order_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                    ),
                    rx.el.div(
                        rx.icon("inbox", class_name="w-16 h-16 text-gray-300 mb-4"),
                        rx.el.h3(
                            "No orders available",
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Please check back later or refresh.",
                            class_name="text-gray-500",
                        ),
                        class_name="flex flex-col items-center justify-center py-16 bg-white rounded-2xl border border-gray-100",
                    ),
                ),
            )
        )
    )