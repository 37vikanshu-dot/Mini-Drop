import reflex as rx
from app.components.shop_owner_layout import shop_owner_layout
from app.states.shop_owner_state import ShopOwnerState
from app.data import ProductDict
from app.components.protected_route import protected_shop_owner


def product_row(product: ProductDict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=product["image_url"],
                    class_name="w-10 h-10 rounded-lg object-cover",
                ),
                rx.el.div(
                    rx.el.p(
                        product["name"], class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p(product["unit"], class_name="text-xs text-gray-500"),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"₹{product['price']}", class_name="text-sm font-bold text-gray-900"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                rx.cond(
                    product["is_available"],
                    rx.el.span(
                        "In Stock",
                        class_name="px-2 py-1 text-xs font-bold text-green-700 bg-green-100 rounded-full",
                    ),
                    rx.el.span(
                        "Out of Stock",
                        class_name="px-2 py-1 text-xs font-bold text-red-700 bg-red-100 rounded-full",
                    ),
                ),
                on_click=ShopOwnerState.toggle_stock(product["id"]),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon(
                    "share_2", class_name="w-4 h-4 text-gray-500 hover:text-[#6200EA]"
                ),
                on_click=ShopOwnerState.open_edit_product_dialog(product),
                class_name="p-2 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
    )


def product_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    rx.cond(
                        ShopOwnerState.editing_product_id == 0,
                        "Add Product",
                        "Edit Product",
                    ),
                    class_name="sr-only",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            rx.cond(
                                ShopOwnerState.editing_product_id == 0,
                                "Add Product",
                                "Edit Product",
                            ),
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5 text-gray-500")
                            )
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Product Name",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                on_change=ShopOwnerState.set_form_name,
                                class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                                placeholder="e.g. Amul Butter",
                                default_value=ShopOwnerState.form_name,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.label(
                                        "Price (₹)",
                                        class_name="block text-sm font-medium text-gray-700 mb-1",
                                    ),
                                    rx.el.input(
                                        on_change=ShopOwnerState.set_form_price,
                                        type="number",
                                        class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                                        placeholder="0.00",
                                        default_value=ShopOwnerState.form_price,
                                    ),
                                    class_name="flex-1 mr-4",
                                ),
                                rx.el.div(
                                    rx.el.label(
                                        "Unit",
                                        class_name="block text-sm font-medium text-gray-700 mb-1",
                                    ),
                                    rx.el.input(
                                        on_change=ShopOwnerState.set_form_unit,
                                        class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                                        placeholder="e.g. 500g",
                                        default_value=ShopOwnerState.form_unit,
                                    ),
                                    class_name="flex-1",
                                ),
                            ),
                            class_name="flex mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Image URL",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                on_change=ShopOwnerState.set_form_image_url,
                                class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                                placeholder="https://...",
                                default_value=ShopOwnerState.form_image_url,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Description",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.textarea(
                                on_change=ShopOwnerState.set_form_description,
                                class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                                rows=3,
                                placeholder="Product details...",
                                default_value=ShopOwnerState.form_description,
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.button(
                            "Save Product",
                            on_click=ShopOwnerState.save_product,
                            class_name="w-full bg-[#6200EA] text-white font-bold py-2.5 rounded-xl hover:bg-[#5000CA] transition-colors",
                        ),
                    ),
                    class_name="bg-white rounded-2xl p-6 w-full shadow-2xl",
                ),
                class_name="fixed left-[50%] top-[50%] z-50 max-h-[85vh] w-[90vw] max-w-md translate-x-[-50%] translate-y-[-50%] focus:outline-none",
            ),
        ),
        open=ShopOwnerState.is_product_dialog_open,
        on_open_change=ShopOwnerState.set_product_dialog_open,
    )


def products_page() -> rx.Component:
    return protected_shop_owner(
        shop_owner_layout(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("Products", class_name="text-2xl font-bold text-gray-900"),
                    rx.el.button(
                        rx.icon("plus", class_name="w-4 h-4 mr-2"),
                        "Add Product",
                        on_click=ShopOwnerState.open_add_product_dialog,
                        class_name="flex items-center px-4 py-2 bg-[#6200EA] text-white rounded-xl font-bold text-sm hover:bg-[#5000CA] shadow-sm hover:shadow-md transition-all",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Product",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Price",
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
                            rx.foreach(ShopOwnerState.products, product_row),
                            class_name="bg-white divide-y divide-gray-100",
                        ),
                        class_name="min-w-full",
                    ),
                    class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
                ),
                product_dialog(),
            )
        )
    )