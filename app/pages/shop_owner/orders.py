import reflex as rx
from app.components.shop_owner_layout import shop_owner_layout
from app.states.shop_owner_state import ShopOwnerState
from app.data import OrderDict
from app.components.protected_route import protected_shop_owner


def order_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.span(f"{item['quantity']}x", class_name="font-bold text-[#6200EA] mr-2"),
        rx.el.span(item["name"], class_name="text-gray-700"),
        class_name="text-sm mb-1",
    )


def order_card(order: OrderDict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h4(f"#{order['id']}", class_name="font-bold text-gray-900"),
                    rx.el.span(
                        order["time"],
                        class_name="text-xs text-gray-500 ml-2 bg-gray-100 px-2 py-0.5 rounded-full",
                    ),
                    class_name="flex items-center mb-1",
                ),
                rx.el.p(
                    f"Total: ₹{order['total_amount']}",
                    class_name="text-sm font-bold text-[#6200EA]",
                ),
            ),
            rx.el.span(
                order["status"],
                class_name=rx.cond(
                    order["status"] == "Pending",
                    "px-3 py-1 rounded-full text-xs font-bold bg-yellow-100 text-yellow-700",
                    "px-3 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700",
                ),
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.p(
                "Items:", class_name="text-xs font-bold text-gray-400 uppercase mb-2"
            ),
            rx.foreach(order["items"], order_item),
            class_name="bg-gray-50 p-3 rounded-lg mb-4",
        ),
        rx.el.div(
            rx.cond(
                order["status"] == "Pending",
                rx.el.div(
                    rx.el.button(
                        "Reject",
                        on_click=ShopOwnerState.update_order_status(
                            order["id"], "Rejected"
                        ),
                        class_name="flex-1 py-2 border border-red-200 text-red-600 font-bold rounded-lg hover:bg-red-50 mr-2",
                    ),
                    rx.el.button(
                        "Accept Order",
                        on_click=ShopOwnerState.update_order_status(
                            order["id"], "Confirmed"
                        ),
                        class_name="flex-1 py-2 bg-[#6200EA] text-white font-bold rounded-lg hover:bg-[#5000CA]",
                    ),
                    class_name="flex",
                ),
            ),
            rx.cond(
                order["status"] == "Confirmed",
                rx.el.button(
                    "Mark Ready to Pick",
                    on_click=ShopOwnerState.update_order_status(order["id"], "Ready"),
                    class_name="w-full py-2 bg-[#6200EA] text-white font-bold rounded-lg hover:bg-[#5000CA]",
                ),
            ),
            rx.cond(
                order["status"] == "Ready",
                rx.el.button(
                    "Mark Handed Over",
                    on_click=ShopOwnerState.update_order_status(
                        order["id"], "Out for Delivery"
                    ),
                    class_name="w-full py-2 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700",
                ),
            ),
            rx.cond(
                order["status"] == "Out for Delivery",
                rx.el.button(
                    "Mark Completed",
                    on_click=ShopOwnerState.update_order_status(
                        order["id"], "Completed"
                    ),
                    class_name="w-full py-2 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700",
                ),
            ),
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm",
    )


def orders_page() -> rx.Component:
    return protected_shop_owner(
        shop_owner_layout(
            rx.el.div(
                rx.el.h1("Orders", class_name="text-2xl font-bold text-gray-900 mb-6"),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "New Requests",
                            class_name="text-lg font-bold text-gray-800 mb-4",
                        ),
                        rx.cond(
                            ShopOwnerState.pending_orders.length() > 0,
                            rx.el.div(
                                rx.foreach(ShopOwnerState.pending_orders, order_card),
                                class_name="grid grid-cols-1 lg:grid-cols-2 gap-4",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "No new orders",
                                    class_name="text-gray-400 text-sm italic",
                                ),
                                class_name="py-8 text-center bg-white rounded-xl border border-dashed border-gray-200",
                            ),
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Ongoing", class_name="text-lg font-bold text-gray-800 mb-4"
                        ),
                        rx.cond(
                            ShopOwnerState.active_orders.length() > 0,
                            rx.el.div(
                                rx.foreach(ShopOwnerState.active_orders, order_card),
                                class_name="grid grid-cols-1 lg:grid-cols-2 gap-4",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "No active orders",
                                    class_name="text-gray-400 text-sm italic",
                                ),
                                class_name="py-8 text-center bg-white rounded-xl border border-dashed border-gray-200",
                            ),
                        ),
                    ),
                ),
            )
        )
    )