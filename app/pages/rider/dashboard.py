import reflex as rx
from app.components.rider_layout import rider_layout
from app.states.rider_state import RiderState
from app.components.protected_route import protected_rider


def stat_card(title: str, value: str, icon: str, color: str = "purple") -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
            ),
            rx.el.div(
                rx.icon(icon, class_name=f"w-6 h-6 text-{color}-600"),
                class_name=f"w-12 h-12 bg-{color}-50 rounded-xl flex items-center justify-center",
            ),
            class_name="flex justify-between items-start",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm",
    )


def dashboard_page() -> rx.Component:
    return protected_rider(
        rider_layout(
            rx.el.div(
                rx.el.h1(
                    "Rider Dashboard",
                    class_name="text-2xl font-bold text-gray-900 mb-6",
                ),
                rx.el.div(
                    stat_card(
                        "Total Earnings",
                        f"₹{RiderState.rider['earnings']}",
                        "wallet",
                        "green",
                    ),
                    stat_card(
                        "Completed Orders",
                        RiderState.rider["completed_orders"].to_string(),
                        "check_check",
                        "blue",
                    ),
                    stat_card(
                        "Current Status",
                        rx.cond(RiderState.is_online, "Online", "Offline"),
                        "power",
                        rx.cond(RiderState.is_online, "green", "gray"),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Recent Activity",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.cond(
                        RiderState.completed_orders_history.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                RiderState.completed_orders_history,
                                lambda order: rx.el.div(
                                    rx.el.div(
                                        rx.el.p(
                                            f"Order #{order['id']}",
                                            class_name="font-bold text-gray-900",
                                        ),
                                        rx.el.p(
                                            order["date"],
                                            class_name="text-xs text-gray-500",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            "Delivered",
                                            class_name="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full",
                                        )
                                    ),
                                    class_name="flex justify-between items-center p-4 bg-white border border-gray-100 rounded-xl mb-2",
                                ),
                            )
                        ),
                        rx.el.p(
                            "No recent activity", class_name="text-gray-500 italic"
                        ),
                    ),
                ),
            )
        )
    )