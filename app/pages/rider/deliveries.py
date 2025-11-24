import reflex as rx
from app.components.rider_layout import rider_layout
from app.states.rider_state import RiderState
from app.components.protected_route import protected_rider
from app.data import OrderDict


def active_delivery_card(order: OrderDict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    f"Delivery #{order['id']}", class_name="font-bold text-gray-900"
                ),
                rx.el.span(
                    "In Progress",
                    class_name="text-xs font-bold px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.el.p(
                    "Delivery Address:",
                    class_name="text-xs font-bold text-gray-500 uppercase mb-1",
                ),
                rx.el.p(
                    order["delivery_address"],
                    class_name="text-sm text-gray-900 font-medium mb-4",
                ),
                rx.el.div(
                    rx.el.a(
                        rx.el.button(
                            rx.icon("map-pin", class_name="w-4 h-4 mr-2"),
                            "Navigate",
                            class_name="flex-1 flex items-center justify-center border border-gray-200 py-2 rounded-lg font-bold text-gray-700 hover:bg-gray-50 mr-2",
                        ),
                        href=f"https://www.google.com/maps/search/?api=1&query={order['delivery_address']}",
                        target="_blank",
                        class_name="flex-1",
                    ),
                    rx.el.button(
                        "Mark Delivered",
                        on_click=RiderState.mark_delivered(order["id"]),
                        class_name="flex-1 bg-green-600 text-white py-2 rounded-lg font-bold hover:bg-green-700 transition-colors",
                    ),
                    class_name="flex",
                ),
            ),
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-md border-l-4 border-l-[#6200EA]",
    )


def deliveries_page() -> rx.Component:
    return protected_rider(
        rider_layout(
            rx.el.div(
                rx.el.h1(
                    "My Deliveries", class_name="text-2xl font-bold text-gray-900 mb-6"
                ),
                rx.el.div(
                    rx.el.h2(
                        "Active Deliveries",
                        class_name="text-lg font-bold text-gray-800 mb-4",
                    ),
                    rx.cond(
                        RiderState.assigned_orders.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                RiderState.assigned_orders, active_delivery_card
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8",
                        ),
                        rx.el.p(
                            "No active deliveries at the moment.",
                            class_name="text-gray-500 mb-8 italic",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.h2(
                        "Completed Today",
                        class_name="text-lg font-bold text-gray-800 mb-4",
                    ),
                    rx.cond(
                        RiderState.completed_orders_history.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                RiderState.completed_orders_history,
                                lambda order: rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            f"#{order['id']}",
                                            class_name="font-bold text-gray-900",
                                        ),
                                        rx.el.span(
                                            "Delivered",
                                            class_name="text-xs font-bold text-green-600",
                                        ),
                                        class_name="flex justify-between",
                                    ),
                                    class_name="p-4 bg-gray-50 rounded-xl border border-gray-100",
                                ),
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                        ),
                        rx.el.p(
                            "No completed orders yet.",
                            class_name="text-gray-500 italic",
                        ),
                    ),
                ),
            )
        )
    )