import reflex as rx
from app.states.rider_state import RiderState


def sidebar_item(label: str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="w-5 h-5"),
        rx.el.span(label, class_name="font-medium"),
        href=href,
        class_name="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-purple-50 hover:text-[#6200EA] rounded-xl transition-colors",
    )


def rider_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.aside(
            rx.el.div(
                rx.el.h1(
                    "Rider Panel",
                    class_name="text-xl font-bold text-[#6200EA] px-4 mb-8",
                ),
                rx.el.nav(
                    sidebar_item("Dashboard", "layout-dashboard", "/rider/dashboard"),
                    sidebar_item("Available Orders", "shopping-bag", "/rider/orders"),
                    sidebar_item("My Deliveries", "bike", "/rider/deliveries"),
                    sidebar_item("Earnings", "wallet", "/rider/earnings"),
                    class_name="flex flex-col gap-1",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            RiderState.rider["name"],
                            class_name="text-sm font-bold text-gray-900 truncate",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name=rx.cond(
                                    RiderState.is_online,
                                    "w-2 h-2 rounded-full bg-green-500 mr-2",
                                    "w-2 h-2 rounded-full bg-gray-400 mr-2",
                                )
                            ),
                            rx.el.p(
                                rx.cond(RiderState.is_online, "Online", "Offline"),
                                class_name="text-xs text-gray-500",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="overflow-hidden",
                    ),
                    rx.el.button(
                        rx.icon(
                            "power",
                            class_name=rx.cond(
                                RiderState.is_online,
                                "w-5 h-5 text-green-500",
                                "w-5 h-5 text-gray-400",
                            ),
                        ),
                        on_click=RiderState.toggle_status,
                        class_name="ml-auto p-2 hover:bg-gray-100 rounded-full transition-colors",
                        title="Toggle Online/Offline",
                    ),
                    class_name="flex items-center p-4 bg-gray-50 rounded-xl",
                ),
                class_name="mt-auto",
            ),
            class_name="fixed left-0 top-0 bottom-0 w-64 bg-white border-r border-gray-100 p-6 flex flex-col z-50 hidden md:flex",
        ),
        rx.el.main(
            content, class_name="md:ml-64 min-h-screen bg-gray-50 p-6 pb-24 md:pb-6"
        ),
        class_name="font-['Lora']",
    )