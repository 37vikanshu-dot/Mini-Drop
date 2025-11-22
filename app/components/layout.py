import reflex as rx
from app.states.main_state import AppState
from app.states.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.h1(
                        "Mini Drop",
                        class_name="font-['Lora'] text-2xl font-bold text-[#6200EA] tracking-tight",
                    ),
                    href="/",
                ),
                rx.el.div(
                    rx.icon("map-pin", class_name="w-3 h-3 text-gray-500"),
                    rx.el.span(
                        "123, Main Street, New York",
                        class_name="text-xs text-gray-500 truncate max-w-[150px]",
                    ),
                    class_name="flex items-center gap-1 mt-1",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("search", class_name="w-5 h-5 text-gray-400 ml-3"),
                    rx.el.input(
                        placeholder="Search for items or shops...",
                        class_name="w-full bg-transparent border-none focus:ring-0 text-sm text-gray-700 placeholder-gray-400 h-10 pl-2",
                        on_change=AppState.update_search.debounce(500),
                    ),
                    class_name="flex items-center bg-gray-100 rounded-full w-full max-w-md border border-transparent focus-within:border-[#6200EA] focus-within:bg-white transition-all duration-200",
                ),
                class_name="hidden md:flex flex-1 justify-center px-8",
            ),
            rx.el.div(
                rx.el.a(
                    rx.el.button(
                        rx.icon("shopping-bag", class_name="w-6 h-6 text-gray-700"),
                        rx.cond(
                            AppState.cart_count > 0,
                            rx.el.span(
                                AppState.cart_count,
                                class_name="absolute -top-1 -right-1 bg-[#6200EA] text-white text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center border-2 border-white",
                            ),
                            None,
                        ),
                        class_name="relative p-2 hover:bg-gray-100 rounded-full transition-colors",
                    ),
                    href="/cart",
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.el.a(
                            rx.el.button(
                                rx.image(
                                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AppState.user_name}",
                                    class_name="w-8 h-8 rounded-full bg-gray-200 border border-gray-200",
                                ),
                                class_name="ml-2",
                            ),
                            href="/account",
                        ),
                        rx.el.button(
                            rx.icon("log-out", class_name="w-4 h-4 text-gray-500"),
                            on_click=AuthState.logout,
                            class_name="ml-2 p-2 hover:bg-red-50 hover:text-red-600 rounded-full transition-colors",
                            title="Logout",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Login",
                            class_name="ml-4 bg-[#6200EA] text-white text-xs font-bold px-4 py-2 rounded-full hover:bg-[#5000CA] transition-colors",
                        ),
                        href="/login",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between max-w-6xl mx-auto px-4 py-3",
        ),
        class_name="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-100 shadow-sm",
    )


def mobile_bottom_nav() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("home", class_name="w-6 h-6 mb-1"),
                    rx.el.span("Home", class_name="text-[10px] font-medium"),
                    class_name="flex flex-col items-center justify-center text-[#6200EA]",
                ),
                href="/",
                class_name="flex-1 py-2",
            ),
            rx.el.a(
                rx.el.div(
                    rx.icon("store", class_name="w-6 h-6 mb-1 text-gray-500"),
                    rx.el.span(
                        "Shops", class_name="text-[10px] font-medium text-gray-500"
                    ),
                    class_name="flex flex-col items-center justify-center hover:text-[#6200EA] transition-colors",
                ),
                href="/shops",
                class_name="flex-1 py-2",
            ),
            rx.el.a(
                rx.el.div(
                    rx.icon("search", class_name="w-6 h-6 mb-1 text-gray-500"),
                    rx.el.span(
                        "Search", class_name="text-[10px] font-medium text-gray-500"
                    ),
                    class_name="flex flex-col items-center justify-center hover:text-[#6200EA] transition-colors",
                ),
                href="/shops",
                class_name="flex-1 py-2",
            ),
            rx.el.a(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "shopping-bag", class_name="w-6 h-6 mb-1 text-gray-500"
                        ),
                        rx.cond(
                            AppState.cart_count > 0,
                            rx.el.span(
                                AppState.cart_count,
                                class_name="absolute top-1 right-8 bg-[#6200EA] text-white text-[9px] font-bold h-3 w-3 rounded-full flex items-center justify-center",
                            ),
                            None,
                        ),
                        class_name="relative flex flex-col items-center",
                    ),
                    rx.el.span(
                        "Cart", class_name="text-[10px] font-medium text-gray-500"
                    ),
                    class_name="flex flex-col items-center justify-center hover:text-[#6200EA] transition-colors",
                ),
                href="/cart",
                class_name="flex-1 py-2",
            ),
            class_name="flex items-center justify-between max-w-md mx-auto",
        ),
        class_name="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 pb-safe pt-1 md:hidden z-50",
    )


def layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(content, class_name="min-h-screen bg-gray-50 pb-24 pt-4"),
        mobile_bottom_nav(),
        class_name="font-['Lora'] text-gray-800",
    )