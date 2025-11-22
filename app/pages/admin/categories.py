import reflex as rx
from app.components.admin_layout import admin_layout
from app.states.admin_state import AdminState
from app.states.auth_state import AuthState
from app.data import CategoryDict


def loading_screen() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.spinner(size="3", class_name="text-[#6200EA] mb-4"),
            rx.el.p(
                "Loading categories...",
                class_name="text-gray-500 font-medium animate-pulse",
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


def category_row(category: CategoryDict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.icon(category["icon"], class_name="w-5 h-5 text-gray-600"),
                    class_name=f"w-10 h-10 rounded-full {category['color_bg']} flex items-center justify-center mr-3",
                ),
                rx.el.div(
                    rx.el.p(
                        category["name"], class_name="text-sm font-bold text-gray-900"
                    ),
                    rx.el.p(category["slug"], class_name="text-xs text-gray-500"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                category["icon"],
                class_name="text-sm text-gray-600 font-mono bg-gray-50 px-2 py-1 rounded",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    class_name=f"w-4 h-4 rounded-full {category['color_bg']} border border-gray-200 mr-2"
                ),
                rx.el.span(category["color_bg"], class_name="text-sm text-gray-500"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                rx.cond(
                    category.get("is_active", True),
                    rx.el.span(
                        "Active",
                        class_name="px-2 py-1 text-xs font-bold text-green-700 bg-green-100 rounded-full",
                    ),
                    rx.el.span(
                        "Inactive",
                        class_name="px-2 py-1 text-xs font-bold text-gray-600 bg-gray-100 rounded-full",
                    ),
                ),
                on_click=AdminState.toggle_category_status(category["id"]),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4 text-gray-500"),
                    on_click=AdminState.open_edit_category_dialog(category),
                    class_name="p-2 hover:bg-gray-100 rounded-lg transition-colors mr-1",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4 text-red-500"),
                    on_click=AdminState.delete_category(category["id"]),
                    class_name="p-2 hover:bg-red-50 rounded-lg transition-colors",
                ),
                class_name="flex justify-end",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
    )


def category_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    rx.cond(
                        AdminState.editing_category_id == 0,
                        "Add Category",
                        "Edit Category",
                    ),
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Name",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. Groceries",
                            on_change=AdminState.set_category_form_name,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-4",
                            default_value=AdminState.category_form_name,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Slug",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. groceries",
                            on_change=AdminState.set_category_form_slug,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-4",
                            default_value=AdminState.category_form_slug,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Icon Name (Lucide)",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. shopping-basket",
                            on_change=AdminState.set_category_form_icon,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-4",
                            default_value=AdminState.category_form_icon,
                        ),
                        rx.el.p(
                            "Use valid Lucide icon names like 'shopping-basket', 'cookie', 'milk'",
                            class_name="text-xs text-gray-500 mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Background Color Class",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Green", value="bg-green-100"),
                            rx.el.option("Blue", value="bg-blue-100"),
                            rx.el.option("Red", value="bg-red-100"),
                            rx.el.option("Yellow", value="bg-yellow-100"),
                            rx.el.option("Orange", value="bg-orange-100"),
                            rx.el.option("Purple", value="bg-purple-100"),
                            rx.el.option("Pink", value="bg-pink-100"),
                            rx.el.option("Gray", value="bg-gray-100"),
                            value=AdminState.category_form_color,
                            on_change=AdminState.set_category_form_color,
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
                            "Save Category",
                            on_click=AdminState.save_category,
                            class_name="px-4 py-2 bg-[#6200EA] text-white text-sm font-bold rounded-lg hover:bg-[#5000CA]",
                        ),
                        class_name="flex justify-end",
                    ),
                ),
                class_name="fixed left-[50%] top-[50%] z-50 max-h-[85vh] w-[90vw] max-w-md translate-x-[-50%] translate-y-[-50%] bg-white rounded-2xl p-6 shadow-2xl focus:outline-none",
            ),
        ),
        open=AdminState.is_category_dialog_open,
        on_open_change=AdminState.set_category_dialog_open,
    )


def categories_content() -> rx.Component:
    return admin_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Manage Categories", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    "Add Category",
                    on_click=AdminState.open_add_category_dialog,
                    class_name="flex items-center px-4 py-2 bg-[#6200EA] text-white rounded-xl font-bold text-sm hover:bg-[#5000CA] shadow-sm hover:shadow-md transition-all",
                ),
                class_name="flex justify-between items-center mb-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Category",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Icon",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Color",
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
                        rx.foreach(AdminState.categories, category_row),
                        class_name="bg-white divide-y divide-gray-100",
                    ),
                    class_name="min-w-full",
                ),
                class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
            ),
            category_dialog(),
        )
    )


from app.components.protected_route import protected_admin


def categories_page() -> rx.Component:
    return protected_admin(categories_content())