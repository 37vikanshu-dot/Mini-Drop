import reflex as rx
from app.states.auth_state import AuthState
from reflex_google_auth import google_login, google_oauth_provider


def login_page() -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        rx.el.div(
            rx.el.div(
                rx.spinner(size="3", class_name="text-[#6200EA]"),
                rx.el.p(
                    "Redirecting...",
                    class_name="text-gray-500 mt-2 font-medium text-sm",
                ),
                class_name="flex flex-col items-center justify-center min-h-screen bg-gray-50",
            ),
            rx.script("setTimeout(() => window.location.href = '/', 100)"),
        ),
        google_oauth_provider(
            rx.el.div(
                rx.el.div(
                    rx.el.a(
                        rx.el.h1(
                            "Mini Drop",
                            class_name="font-['Lora'] text-4xl font-bold text-[#6200EA] tracking-tight text-center mb-8",
                        ),
                        href="/",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Welcome Back",
                                class_name="text-2xl font-bold text-gray-900 mb-2",
                            ),
                            rx.el.p(
                                "Sign in to continue ordering",
                                class_name="text-sm text-gray-500 mb-8",
                            ),
                            rx.el.div(
                                google_login(), class_name="flex justify-center mb-6"
                            ),
                            rx.el.div(
                                rx.el.div(class_name="h-px bg-gray-200 flex-1"),
                                rx.el.span(
                                    "OR", class_name="text-xs text-gray-400 px-3"
                                ),
                                rx.el.div(class_name="h-px bg-gray-200 flex-1"),
                                class_name="flex items-center mb-6",
                            ),
                            rx.cond(
                                AuthState.error_message != "",
                                rx.el.div(
                                    rx.icon("circle-alert", class_name="w-4 h-4 mr-2"),
                                    rx.el.span(AuthState.error_message),
                                    class_name="bg-red-50 text-red-600 p-3 rounded-xl text-sm font-medium flex items-center mb-6",
                                ),
                                None,
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Email Address",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    type="email",
                                    placeholder="your@email.com",
                                    on_change=AuthState.set_login_email,
                                    class_name="w-full rounded-xl border border-gray-300 px-4 py-2.5 text-sm focus:ring-2 focus:ring-[#6200EA] focus:border-transparent outline-none transition-all",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.label(
                                        "Password",
                                        class_name="block text-sm font-medium text-gray-700",
                                    ),
                                    rx.el.a(
                                        "Forgot Password?",
                                        href="#",
                                        class_name="text-xs font-bold text-[#6200EA] hover:text-[#5000CA]",
                                    ),
                                    class_name="flex justify-between items-center mb-1",
                                ),
                                rx.el.input(
                                    type="password",
                                    placeholder="••••••••",
                                    on_change=AuthState.set_login_password,
                                    class_name="w-full rounded-xl border border-gray-300 px-4 py-2.5 text-sm focus:ring-2 focus:ring-[#6200EA] focus:border-transparent outline-none transition-all",
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.button(
                                "Sign In",
                                on_click=AuthState.login,
                                class_name="w-full bg-[#6200EA] text-white py-3 rounded-xl font-bold hover:bg-[#5000CA] transition-all shadow-lg shadow-purple-200 active:scale-[0.98]",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Don't have an account? ",
                                    class_name="text-gray-500",
                                ),
                                rx.el.a(
                                    "Register",
                                    href="/register",
                                    class_name="text-[#6200EA] font-bold hover:underline",
                                ),
                                class_name="text-center text-sm mt-6",
                            ),
                            class_name="bg-white p-8 rounded-3xl shadow-xl shadow-gray-100 border border-gray-100",
                        ),
                        class_name="w-full max-w-md px-4",
                    ),
                    class_name="flex flex-col items-center justify-center w-full",
                ),
                class_name="min-h-screen bg-gray-50 flex items-center justify-center w-full",
            )
        ),
    )