import reflex as rx
from app.states.shop_owner_state import ShopOwnerState


def sidebar_item(label: str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="w-5 h-5"),
        rx.el.span(label, class_name="font-medium"),
        href=href,
        class_name="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-purple-50 hover:text-[#6200EA] rounded-xl transition-colors",
    )


def shop_owner_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.aside(
            rx.el.div(
                rx.el.h1(
                    "Partner Panel",
                    class_name="text-xl font-bold text-[#6200EA] px-4 mb-8",
                ),
                rx.el.nav(
                    sidebar_item(
                        "Dashboard", "layout-dashboard", "/shop-owner/dashboard"
                    ),
                    sidebar_item("Products", "package", "/shop-owner/products"),
                    sidebar_item("Orders", "shopping-bag", "/shop-owner/orders"),
                    sidebar_item("Payouts", "wallet", "/shop-owner/payouts"),
                    class_name="flex flex-col gap-1",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src="https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=100&q=80",
                        class_name="w-10 h-10 rounded-full object-cover",
                    ),
                    rx.el.div(
                        rx.el.p(
                            ShopOwnerState.shop_name,
                            class_name="text-sm font-bold text-gray-900 truncate",
                        ),
                        rx.el.p("Shop Owner", class_name="text-xs text-gray-500"),
                        class_name="ml-3 overflow-hidden",
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