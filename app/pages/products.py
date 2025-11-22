import reflex as rx
from app.components.layout import layout
from app.components.cards import product_card
from app.states.main_state import AppState


def back_button() -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon("arrow-left", class_name="w-5 h-5 text-gray-700"),
            rx.el.span(
                "Back to Shops", class_name="text-sm font-medium text-gray-700 ml-2"
            ),
            class_name="flex items-center mb-6 hover:text-[#6200EA] transition-colors cursor-pointer w-fit",
        ),
        href="/shops",
    )


def shop_info_badge(icon: str, text: str, color: str = "gray") -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name=f"w-4 h-4 text-{color}-500 mr-1.5"),
        rx.el.span(text, class_name=f"text-sm text-{color}-700 font-medium"),
        class_name=f"flex items-center bg-{color}-50 px-3 py-1.5 rounded-full border border-{color}-100",
    )


def shop_header() -> rx.Component:
    shop = AppState.current_shop
    return rx.el.div(
        rx.el.div(
            rx.image(src=shop["image_url"], class_name="w-full h-full object-cover"),
            rx.el.div(
                class_name="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"
            ),
            rx.el.div(
                rx.cond(
                    shop["is_featured"],
                    rx.el.span(
                        "Featured",
                        class_name="bg-[#6200EA] text-white text-xs font-bold px-3 py-1 rounded-full shadow-sm",
                    ),
                    rx.fragment(),
                ),
                class_name="absolute top-4 right-4",
            ),
            class_name="h-48 md:h-64 w-full relative overflow-hidden rounded-t-2xl md:rounded-2xl",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    shop["name"],
                    class_name="text-2xl md:text-3xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(shop["address"], class_name="text-gray-500 text-sm mb-4"),
                rx.el.div(
                    shop_info_badge("star", shop["rating"].to_string(), "yellow"),
                    shop_info_badge("clock", shop["delivery_time"], "blue"),
                    shop_info_badge("map-pin", shop["distance"], "purple"),
                    class_name="flex flex-wrap gap-3",
                ),
                class_name="flex-1",
            ),
            class_name="p-6 md:p-8 -mt-10 relative bg-white rounded-t-3xl md:rounded-3xl mx-0 md:mx-6 shadow-sm border border-gray-100 md:-mt-12",
        ),
        class_name="mb-8",
    )


def products_grid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Menu", class_name="text-xl font-bold text-gray-900"),
            rx.el.span(
                f"{AppState.shop_products.length()} items",
                class_name="text-sm text-gray-500 font-medium bg-gray-100 px-2 py-1 rounded-lg",
            ),
            class_name="flex justify-between items-center mb-6 pb-4 border-b border-gray-100",
        ),
        rx.cond(
            AppState.shop_products.length() > 0,
            rx.el.div(
                rx.foreach(AppState.shop_products, product_card),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
            ),
            rx.el.div(
                rx.icon("package-open", class_name="w-16 h-16 text-gray-200 mb-4"),
                rx.el.p(
                    "No products available yet.", class_name="text-gray-500 font-medium"
                ),
                class_name="flex flex-col items-center justify-center py-16 bg-gray-50 rounded-2xl border border-dashed border-gray-200",
            ),
        ),
    )


def products_page() -> rx.Component:
    return layout(
        rx.el.div(
            back_button(),
            rx.cond(
                AppState.current_shop,
                rx.el.div(
                    shop_header(),
                    products_grid(),
                    class_name="animate-in fade-in duration-500",
                ),
                rx.el.div(
                    rx.cond(
                        AppState.shops.length() > 0,
                        rx.el.div(
                            rx.icon("store", class_name="w-20 h-20 text-gray-200 mb-4"),
                            rx.el.h3(
                                "Shop not found",
                                class_name="text-xl font-bold text-gray-900 mb-2",
                            ),
                            rx.el.p(
                                "The shop you are looking for might have been removed or is temporarily unavailable.",
                                class_name="text-gray-500 text-center max-w-md mb-8",
                            ),
                            rx.el.a(
                                rx.el.button(
                                    "Browse Other Shops",
                                    class_name="bg-[#6200EA] text-white px-6 py-3 rounded-xl font-bold shadow-lg hover:bg-[#5000CA] transition-all",
                                ),
                                href="/shops",
                            ),
                            class_name="flex flex-col items-center justify-center py-20",
                        ),
                        rx.el.div(
                            rx.spinner(size="3", class_name="text-[#6200EA]"),
                            rx.el.p(
                                "Loading shop details...",
                                class_name="text-gray-500 mt-4 font-medium animate-pulse",
                            ),
                            class_name="flex flex-col items-center justify-center py-32",
                        ),
                    )
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        )
    )