import reflex as rx
from app.components.admin_layout import admin_layout
from app.states.admin_state import AdminState
from app.data import OrderDict
from app.components.protected_route import protected_admin


def order_row(order: OrderDict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"#{order['id']}", class_name="text-sm font-bold text-gray-900"
                ),
                rx.el.p(order["date"], class_name="text-xs text-gray-500"),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"₹{order['total_amount']}",
                class_name="text-sm font-bold text-[#6200EA]",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(order["delivery_address"], class_name="text-sm text-gray-600"),
            class_name="px-6 py-4 max-w-xs truncate",
        ),
        rx.el.td(
            rx.el.span(
                order["status"],
                class_name=rx.cond(
                    order["status"] == "Pending",
                    "bg-yellow-100 text-yellow-800",
                    rx.cond(
                        order["status"] == "Delivered",
                        "bg-green-100 text-green-800",
                        "bg-blue-100 text-blue-800",
                    ),
                )
                + " px-2 py-1 text-xs font-bold rounded-full",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                "Manage",
                class_name="text-xs font-bold text-[#6200EA] bg-purple-50 px-3 py-1.5 rounded-lg hover:bg-purple-100",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
    )


def orders_page() -> rx.Component:
    return protected_admin(
        admin_layout(
            rx.el.div(
                rx.el.h1(
                    "Manage Orders", class_name="text-2xl font-bold text-gray-900 mb-6"
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Order ID",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Amount",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Address",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                            ),
                            class_name="bg-gray-50 border-b border-gray-100",
                        ),
                        rx.el.tbody(
                            rx.foreach(AdminState.orders, order_row),
                            class_name="bg-white divide-y divide-gray-100",
                        ),
                        class_name="min-w-full",
                    ),
                    class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
                ),
            )
        )
    )