import reflex as rx


def sidebar_item(label: str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="w-5 h-5"),
        rx.el.span(label, class_name="font-medium"),
        href=href,
        class_name="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-purple-50 hover:text-[#6200EA] rounded-xl transition-colors",
    )


def admin_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.aside(
            rx.el.div(
                rx.el.h1(
                    "Admin Panel",
                    class_name="text-xl font-bold text-[#6200EA] px-4 mb-8",
                ),
                rx.el.nav(
                    sidebar_item("Dashboard", "layout-dashboard", "/admin/dashboard"),
                    sidebar_item("Categories", "layout-grid", "/admin/categories"),
                    sidebar_item("Shops", "store", "/admin/shops"),
                    sidebar_item("Orders", "shopping-bag", "/admin/orders"),
                    sidebar_item("Delivery Partners", "bike", "/admin/riders"),
                    sidebar_item("Pricing", "tag", "/admin/pricing"),
                    sidebar_item("Reports", "bar-chart-2", "/admin/reports"),
                    class_name="flex flex-col gap-1",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src="https://api.dicebear.com/9.x/notionists/svg?seed=Admin",
                        class_name="w-10 h-10 rounded-full object-cover bg-gray-200",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Super Admin",
                            class_name="text-sm font-bold text-gray-900 truncate",
                        ),
                        rx.el.p(
                            "admin@minidrop.com", class_name="text-xs text-gray-500"
                        ),
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