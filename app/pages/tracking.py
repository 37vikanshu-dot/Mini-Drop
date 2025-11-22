import reflex as rx
from app.components.layout import layout
from app.states.main_state import AppState


def status_step(
    label: str, is_completed: bool, is_active: bool, is_last: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    is_completed,
                    rx.icon("check", class_name="w-4 h-4 text-white"),
                    rx.el.div(
                        class_name=f"w-2 h-2 rounded-full {('bg-[#6200EA]' if is_active else 'bg-gray-300')}"
                    ),
                ),
                class_name=rx.cond(
                    is_completed,
                    "w-8 h-8 rounded-full bg-[#6200EA] flex items-center justify-center z-10",
                    f"w-8 h-8 rounded-full {('bg-purple-100 border-2 border-[#6200EA]' if is_active else 'bg-gray-100 border-2 border-gray-200')} flex items-center justify-center z-10",
                ),
            ),
            rx.cond(
                ~is_last,
                rx.el.div(
                    class_name=rx.cond(
                        is_completed,
                        "absolute top-8 left-4 w-0.5 h-12 bg-[#6200EA] -ml-px",
                        "absolute top-8 left-4 w-0.5 h-12 bg-gray-200 -ml-px",
                    )
                ),
                None,
            ),
            class_name="relative flex flex-col items-center mr-4",
        ),
        rx.el.div(
            rx.el.h4(
                label,
                class_name=rx.cond(
                    is_completed | is_active,
                    "text-sm font-bold text-gray-900",
                    "text-sm font-medium text-gray-500",
                ),
            ),
            rx.cond(
                is_active,
                rx.el.p(
                    "Processing...",
                    class_name="text-xs text-[#6200EA] animate-pulse mt-0.5",
                ),
                None,
            ),
            class_name="pt-1.5 pb-8",
        ),
        class_name="flex",
    )


def tracking_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.cond(
                AppState.active_order,
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Order Tracking",
                            class_name="text-2xl font-bold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            f"Order #{AppState.active_order['id']}",
                            class_name="text-sm text-gray-500 mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Estimated Delivery",
                                    class_name="text-xs text-gray-500 uppercase tracking-wider mb-1",
                                ),
                                rx.el.p(
                                    "15-20 mins",
                                    class_name="text-2xl font-bold text-[#6200EA]",
                                ),
                            ),
                            rx.image(
                                src="https://cdn-icons-png.flaticon.com/512/2830/2830305.png",
                                class_name="w-16 h-16 object-contain",
                            ),
                            class_name="flex justify-between items-center bg-white p-5 rounded-2xl border border-gray-100 shadow-sm mb-8",
                        ),
                        rx.el.div(
                            status_step("Order Confirmed", True, False),
                            status_step("Packed", False, True),
                            status_step("Rider Assigned", False, False),
                            status_step("Out for Delivery", False, False),
                            status_step("Delivered", False, False, is_last=True),
                            class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mb-8",
                        ),
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Order Details",
                            class_name="text-sm font-bold text-gray-900 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                AppState.active_order["items"],
                                lambda item: rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            f"{item['quantity']}x",
                                            class_name="font-bold text-[#6200EA] mr-3",
                                        ),
                                        rx.el.span(
                                            item["name"], class_name="text-gray-800"
                                        ),
                                        class_name="flex items-center",
                                    ),
                                    rx.el.span(
                                        f"₹{item['price'] * item['quantity']}",
                                        class_name="font-medium text-gray-900",
                                    ),
                                    class_name="flex justify-between py-2 border-b border-gray-50 last:border-0",
                                ),
                            ),
                            class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.h1(
                        "Order Not Found", class_name="text-xl font-bold text-gray-900"
                    ),
                    rx.el.a(
                        "Go Home",
                        href="/",
                        class_name="text-[#6200EA] font-bold mt-4 block",
                    ),
                    class_name="text-center py-20",
                ),
            ),
            class_name="max-w-2xl mx-auto px-4",
        )
    )