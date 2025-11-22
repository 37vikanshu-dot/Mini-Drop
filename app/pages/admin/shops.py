import reflex as rx
from app.components.admin_layout import admin_layout
from app.states.admin_state import AdminState
from app.states.auth_state import AuthState
from app.data import ShopDict


def loading_screen() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.spinner(size="3", class_name="text-[#6200EA] mb-4"),
            rx.el.p(
                "Loading shops...", class_name="text-gray-500 font-medium animate-pulse"
            ),
            class_name="flex flex-col items-center justify-center",
        ),
        class_name="min-h-screen bg-gray-50 flex items-center justify-center",
    )


def access_denied_message() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("shield-alert", class_name="w-16 h-16 text-red-500 mb-4"),
            rx.el.h1("Access Denied", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "You don't have admin privileges to view this page.",
                class_name="text-gray-500 mt-2",
            ),
            rx.el.a(
                rx.el.button(
                    "Go Home",
                    class_name="mt-6 bg-[#6200EA] text-white px-6 py-2 rounded-full font-bold text-sm hover:bg-[#5000CA]",
                ),
                href="/",
            ),
            class_name="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4",
        )
    )


def shop_row(shop: ShopDict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=shop["image_url"],
                    class_name="w-10 h-10 rounded-lg object-cover",
                ),
                rx.el.div(
                    rx.el.p(
                        shop["name"], class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p(
                        shop["category_slug"],
                        class_name="text-xs text-gray-500 uppercase",
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                shop["rating"].to_string(),
                rx.icon(
                    "star",
                    class_name="w-3 h-3 inline ml-1 text-yellow-400 fill-yellow-400",
                ),
                class_name="text-sm font-bold text-gray-900 flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span("10%", class_name="text-sm text-gray-600"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                "Active",
                class_name="px-2 py-1 text-xs font-bold text-green-700 bg-green-100 rounded-full",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4 text-gray-500"),
                    on_click=AdminState.open_edit_shop_dialog(shop),
                    class_name="p-2 hover:bg-gray-100 rounded-lg transition-colors mr-1",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4 text-red-500"),
                    on_click=AdminState.delete_shop(shop["id"]),
                    class_name="p-2 hover:bg-red-50 rounded-lg transition-colors",
                ),
                class_name="flex justify-end",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
    )


def shop_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Add New Shop", class_name="text-lg font-bold text-gray-900 mb-4"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Shop Name",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="Enter shop name",
                            on_change=AdminState.set_shop_form_name,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Category",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Grocery", value="grocery"),
                            rx.el.option("Medical", value="medical"),
                            rx.el.option("Dairy", value="dairy"),
                            rx.el.option("Snacks", value="snacks"),
                            rx.el.option("Bakery", value="bakery"),
                            rx.el.option("Stationery", value="stationery"),
                            value=AdminState.shop_form_category,
                            on_change=AdminState.set_shop_form_category,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Address",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. 123 Main St",
                            on_change=AdminState.set_shop_form_address,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-4",
                            default_value=AdminState.shop_form_address,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Image URL",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="https://...",
                            on_change=AdminState.set_shop_form_image_url,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-4",
                            default_value=AdminState.shop_form_image_url,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Commission Rate (%)",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="number",
                            default_value=AdminState.shop_form_commission,
                            on_change=AdminState.set_shop_form_commission,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                class_name="px-4 py-2 text-sm font-bold text-gray-600 hover:bg-gray-100 rounded-lg mr-2",
                            )
                        ),
                        rx.el.button(
                            "Save Shop",
                            on_click=AdminState.save_shop,
                            class_name="px-4 py-2 bg-[#6200EA] text-white text-sm font-bold rounded-lg hover:bg-[#5000CA]",
                        ),
                        class_name="flex justify-end",
                    ),
                ),
                class_name="fixed left-[50%] top-[50%] z-50 max-h-[85vh] w-[90vw] max-w-md translate-x-[-50%] translate-y-[-50%] bg-white rounded-2xl p-6 shadow-2xl focus:outline-none",
            ),
        ),
        open=AdminState.is_shop_dialog_open,
        on_open_change=AdminState.set_shop_dialog_open,
    )


def shops_content() -> rx.Component:
    return admin_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Manage Shops", class_name="text-2xl font-bold text-gray-900"),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    "Add Shop",
                    on_click=AdminState.open_add_shop_dialog,
                    class_name="flex items-center px-4 py-2 bg-[#6200EA] text-white rounded-xl font-bold text-sm hover:bg-[#5000CA] shadow-sm hover:shadow-md transition-all",
                ),
                class_name="flex justify-between items-center mb-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Shop Details",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Rating",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Commission",
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
                        rx.foreach(AdminState.shops, shop_row),
                        class_name="bg-white divide-y divide-gray-100",
                    ),
                    class_name="min-w-full",
                ),
                class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
            ),
            shop_dialog(),
        )
    )


from app.components.protected_route import protected_admin


def shops_page() -> rx.Component:
    return protected_admin(shops_content())