import reflex as rx
from app.components.layout import layout
from app.components.cards import shop_card
from app.states.main_state import AppState


def filter_pill(label: str, slug: str) -> rx.Component:
    is_active = AppState.active_category_filter == slug
    return rx.el.button(
        label,
        on_click=lambda: AppState.set_category_filter(slug),
        class_name=rx.cond(
            is_active,
            "bg-[#6200EA] text-white shadow-md",
            "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50",
        )
        + " px-4 py-2 rounded-full text-xs font-bold transition-all duration-200 whitespace-nowrap flex-shrink-0 mr-2",
    )


def shop_list_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.h2("All Shops", class_name="text-2xl font-bold text-gray-800 mb-6"),
            rx.cond(
                AppState.categories.length() > 0,
                rx.el.div(
                    filter_pill("All", "all"),
                    rx.foreach(
                        AppState.categories,
                        lambda cat: filter_pill(cat["name"], cat["slug"]),
                    ),
                    class_name="flex overflow-x-auto pb-2 scrollbar-hide mb-6 -mx-4 px-4 md:mx-0 md:px-0",
                ),
            ),
            rx.el.div(
                rx.cond(
                    AppState.filtered_shops.length() > 0,
                    rx.el.div(
                        rx.foreach(AppState.filtered_shops, shop_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                    ),
                    rx.cond(
                        AppState.shops.length() == 0,
                        rx.el.div(
                            rx.icon("store", class_name="w-16 h-16 text-gray-300 mb-4"),
                            rx.el.h3(
                                "No shops available",
                                class_name="text-lg font-bold text-gray-900 mb-2",
                            ),
                            rx.el.p(
                                "We are currently onboarding new partners. Please check back later!",
                                class_name="text-gray-500 text-center max-w-sm",
                            ),
                            class_name="flex flex-col items-center justify-center py-16 bg-white rounded-2xl border border-gray-100",
                        ),
                        rx.el.div(
                            rx.icon("store", class_name="w-16 h-16 text-gray-300 mb-4"),
                            rx.el.p(
                                "No shops found in this category.",
                                class_name="text-gray-500",
                            ),
                            class_name="flex flex-col items-center justify-center py-12",
                        ),
                    ),
                )
            ),
            class_name="max-w-4xl mx-auto px-4",
        )
    )