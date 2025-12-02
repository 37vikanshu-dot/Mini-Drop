import reflex as rx
from app.components.layout import layout
from app.components.cards import category_card, shop_card, quick_item_card
from app.states.main_state import AppState
from app.states.ai_state import AIState


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


def genie_input_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "sparkles",
                    class_name="w-5 h-5 text-[#6200EA] absolute left-3 top-3 animate-pulse",
                ),
                rx.el.input(
                    placeholder="✨ Ask AI Genie (e.g., 'I need breakfast for 2')",
                    class_name="w-full bg-white border-none rounded-2xl py-3 pl-10 pr-12 text-sm shadow-sm focus:ring-2 focus:ring-[#6200EA] placeholder-gray-400",
                    on_change=AIState.set_genie_input,
                    on_key_down=AIState.handle_key_down,
                    default_value=AIState.genie_input,
                ),
                rx.el.button(
                    rx.icon("arrow-right", class_name="w-5 h-5 text-white"),
                    on_click=AIState.ask_genie,
                    class_name="absolute right-1.5 top-1.5 bg-[#6200EA] p-1.5 rounded-xl hover:bg-[#5000CA] transition-colors",
                ),
                class_name="relative",
            ),
            class_name="mb-8",
        ),
        genie_modal(),
    )


def genie_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "AI Genie Recommendations",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.cond(
                    AIState.is_loading_genie,
                    rx.el.div(
                        rx.spinner(size="3", class_name="text-[#6200EA] mb-4"),
                        rx.el.p(
                            "Genie is thinking...",
                            class_name="text-gray-500 font-medium animate-pulse",
                        ),
                        class_name="flex flex-col items-center justify-center py-8",
                    ),
                    rx.el.div(
                        rx.cond(
                            AIState.genie_recommendations.length() > 0,
                            rx.el.div(
                                rx.foreach(
                                    AIState.genie_recommendations,
                                    lambda item: rx.el.div(
                                        rx.el.div(
                                            rx.image(
                                                src=item["image_url"],
                                                class_name="w-12 h-12 rounded-lg object-cover",
                                            ),
                                            rx.el.div(
                                                rx.el.p(
                                                    item["name"],
                                                    class_name="text-sm font-bold text-gray-900",
                                                ),
                                                rx.el.p(
                                                    item["reason"],
                                                    class_name="text-xs text-gray-500 line-clamp-2",
                                                ),
                                                class_name="ml-3 flex-1",
                                            ),
                                            class_name="flex items-start",
                                        ),
                                        rx.el.button(
                                            rx.icon("plus", class_name="w-4 h-4 mr-1"),
                                            "Add",
                                            on_click=AIState.add_genie_item_to_cart(
                                                item["id"], item["quantity"]
                                            ),
                                            class_name="mt-2 w-full flex items-center justify-center bg-purple-50 text-[#6200EA] py-1.5 rounded-lg text-xs font-bold hover:bg-purple-100",
                                        ),
                                        class_name="bg-white p-3 rounded-xl border border-gray-100 mb-3",
                                    ),
                                ),
                                class_name="max-h-[60vh] overflow-y-auto",
                            ),
                            rx.el.p(
                                "No recommendations found.",
                                class_name="text-gray-500 text-center py-4",
                            ),
                        ),
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Close",
                                    class_name="w-full bg-gray-100 text-gray-700 font-bold py-2.5 rounded-xl hover:bg-gray-200 transition-colors",
                                )
                            ),
                            class_name="mt-4",
                        ),
                    ),
                ),
                class_name="fixed left-[50%] top-[50%] z-50 max-h-[85vh] w-[90vw] max-w-md translate-x-[-50%] translate-y-[-50%] bg-white rounded-2xl p-6 shadow-2xl focus:outline-none",
            ),
        ),
        open=AIState.is_genie_open,
        on_open_change=AIState.toggle_genie_modal,
    )


def smart_basket_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("AI Smart Basket", class_name="text-lg font-bold text-gray-800"),
            rx.el.button(
                rx.cond(
                    AIState.is_loading_basket,
                    rx.spinner(size="1", class_name="text-[#6200EA]"),
                    rx.icon("sparkles", class_name="w-4 h-4 text-[#6200EA]"),
                ),
                "Generate",
                on_click=AIState.generate_smart_basket,
                disabled=AIState.is_loading_basket,
                class_name="flex items-center gap-2 bg-purple-50 px-3 py-1 rounded-full text-xs font-bold text-[#6200EA] hover:bg-purple-100",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.cond(
            AIState.smart_basket.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        AIState.smart_basket_theme,
                        class_name="text-sm font-medium text-[#6200EA] mb-3",
                    ),
                    rx.el.div(
                        rx.foreach(
                            AIState.smart_basket,
                            lambda item: rx.el.div(
                                rx.image(
                                    src=item["image_url"],
                                    class_name="w-10 h-10 rounded-lg object-cover",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        item["name"],
                                        class_name="text-xs font-bold text-gray-900 truncate",
                                    ),
                                    rx.el.p(
                                        f"Qty: {item['quantity']}",
                                        class_name="text-[10px] text-gray-500",
                                    ),
                                    class_name="ml-2 flex-1 overflow-hidden",
                                ),
                                class_name="flex items-center bg-white p-2 rounded-lg border border-gray-100 min-w-[140px]",
                            ),
                        ),
                        class_name="flex gap-3 overflow-x-auto pb-2 scrollbar-hide",
                    ),
                    class_name="bg-purple-50/50 p-4 rounded-2xl border border-purple-100 mb-4",
                ),
                rx.el.button(
                    "Add All to Cart",
                    on_click=AIState.add_smart_basket_to_cart,
                    class_name="w-full bg-[#6200EA] text-white py-2.5 rounded-xl font-bold text-sm hover:bg-[#5000CA] shadow-md transition-all active:scale-95",
                ),
                class_name="animate-in fade-in slide-in-from-top-4 duration-500 mb-8",
            ),
            rx.cond(
                AIState.is_loading_basket,
                rx.el.div(
                    rx.el.div(
                        class_name="h-32 bg-gray-100 rounded-2xl animate-pulse mb-4"
                    ),
                    class_name="mb-8",
                ),
            ),
        ),
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
                class_name="relative mb-4 md:hidden",
            ),
            hero_section(),
            genie_input_section(),
            smart_basket_section(),
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