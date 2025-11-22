import reflex as rx
from app.components.layout import layout
from app.components.cards import category_card, shop_card, quick_item_card
from app.states.main_state import AppState


def hero_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Super fast delivery", class_name="text-xl font-bold text-white mb-1"
            ),
            rx.el.p(
                "Get groceries in 15 mins", class_name="text-white/90 text-sm mb-4"
            ),
            rx.el.button(
                "Order Now",
                class_name="bg-white text-[#6200EA] px-4 py-2 rounded-full text-xs font-bold shadow-lg hover:scale-105 transition-transform",
            ),
            class_name="bg-gradient-to-r from-[#6200EA] to-[#9046FC] rounded-3xl p-6 shadow-lg shadow-purple-200 relative overflow-hidden",
        ),
        rx.el.div(
            class_name="absolute -right-8 -bottom-8 w-32 h-32 bg-white/20 rounded-full blur-2xl"
        ),
        class_name="mb-8 relative",
    )


def home_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search", class_name="w-5 h-5 text-gray-400 absolute left-3 top-2.5"
                ),
                rx.el.input(
                    placeholder="Search 'milk'",
                    class_name="w-full bg-white border-none rounded-xl py-2.5 pl-10 pr-4 text-sm shadow-sm focus:ring-1 focus:ring-[#6200EA] placeholder-gray-400",
                ),
                class_name="relative mb-6 md:hidden",
            ),
            hero_section(),
            rx.cond(
                AppState.categories.length() > 0,
                rx.el.div(
                    rx.el.h3(
                        "Categories", class_name="text-lg font-bold text-gray-800 mb-4"
                    ),
                    rx.el.div(
                        rx.foreach(AppState.categories, category_card),
                        class_name="grid grid-cols-3 sm:grid-cols-6 gap-4",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Welcome to Mini Drop",
                        class_name="text-lg font-bold text-gray-800 mb-2",
                    ),
                    rx.el.p(
                        "We are setting things up! Check back soon for categories.",
                        class_name="text-sm text-gray-500 mb-8",
                    ),
                ),
            ),
            rx.cond(
                AppState.quick_items.length() > 0,
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Quick Pick", class_name="text-lg font-bold text-gray-800"
                        ),
                        rx.el.a(
                            "See all",
                            href="#",
                            class_name="text-xs text-[#6200EA] font-bold",
                        ),
                        class_name="flex justify-between items-center mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(AppState.quick_items, quick_item_card),
                        class_name="flex overflow-x-auto pb-4 scrollbar-hide -mx-4 px-4",
                    ),
                    class_name="mb-8",
                ),
            ),
            rx.cond(
                AppState.featured_shops.length() > 0,
                rx.el.div(
                    rx.el.h3(
                        "Featured Shops",
                        class_name="text-lg font-bold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(AppState.featured_shops, shop_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                    ),
                    class_name="mb-4",
                ),
                rx.cond(
                    AppState.shops.length() == 0,
                    rx.el.div(
                        rx.icon(
                            "store", class_name="w-16 h-16 text-gray-300 mb-4 mx-auto"
                        ),
                        rx.el.h3(
                            "No Shops Available Yet",
                            class_name="text-lg font-bold text-gray-800 text-center",
                        ),
                        rx.el.p(
                            "Stores will be listed here soon.",
                            class_name="text-gray-500 text-center mt-1",
                        ),
                        class_name="py-12 bg-white rounded-2xl border border-gray-100 shadow-sm",
                    ),
                ),
            ),
            class_name="max-w-4xl mx-auto px-4",
        )
    )