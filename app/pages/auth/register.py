import reflex as rx
from app.states.auth_state import AuthState


def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.el.h1(
                    "Mini Drop",
                    class_name="font-['Lora'] text-3xl font-bold text-[#6200EA] tracking-tight text-center mb-8",
                ),
                href="/",
            ),
            rx.el.div(
                rx.el.h2(
                    "Create Account", class_name="text-2xl font-bold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Join us to start ordering instantly",
                    class_name="text-sm text-gray-500 mb-8",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        rx.icon("badge_alert", class_name="w-4 h-4 mr-2"),
                        rx.el.span(AuthState.error_message),
                        class_name="bg-red-50 text-red-600 p-3 rounded-xl text-sm font-medium flex items-center mb-6",
                    ),
                    None,
                ),
                rx.el.div(
                    rx.el.label(
                        "Full Name",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        placeholder="John Doe",
                        on_change=AuthState.set_register_name,
                        class_name="w-full rounded-xl border border-gray-300 px-4 py-2.5 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Email Address",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="email",
                        placeholder="your@email.com",
                        on_change=AuthState.set_register_email,
                        class_name="w-full rounded-xl border border-gray-300 px-4 py-2.5 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Phone Number",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="tel",
                        placeholder="9876543210",
                        on_change=AuthState.set_register_phone,
                        class_name="w-full rounded-xl border border-gray-300 px-4 py-2.5 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="password",
                        placeholder="Minimum 8 characters",
                        on_change=AuthState.set_register_password,
                        class_name="w-full rounded-xl border border-gray-300 px-4 py-2.5 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Confirm Password",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="password",
                        placeholder="Re-enter password",
                        on_change=AuthState.set_register_confirm_password,
                        class_name="w-full rounded-xl border border-gray-300 px-4 py-2.5 text-sm focus:ring-[#6200EA] focus:border-[#6200EA]",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            on_change=AuthState.toggle_register_terms,
                            class_name="w-4 h-4 text-[#6200EA] border-gray-300 rounded focus:ring-[#6200EA]",
                        ),
                        rx.el.span(
                            "I agree to the Terms & Conditions",
                            class_name="ml-2 text-sm text-gray-600",
                        ),
                        class_name="flex items-center cursor-pointer",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    "Create Account",
                    on_click=AuthState.register,
                    class_name="w-full bg-[#6200EA] text-white py-3 rounded-xl font-bold hover:bg-[#5000CA] transition-colors shadow-lg shadow-purple-200",
                ),
                rx.el.div(
                    rx.el.span("Already have an account? ", class_name="text-gray-500"),
                    rx.el.a(
                        "Sign In", href="/login", class_name="text-[#6200EA] font-bold"
                    ),
                    class_name="text-center text-sm mt-6",
                ),
                class_name="bg-white p-8 rounded-3xl shadow-sm border border-gray-100",
            ),
            class_name="w-full max-w-md px-4",
        ),
        class_name="min-h-screen bg-gray-50 flex items-center justify-center py-12",
    )