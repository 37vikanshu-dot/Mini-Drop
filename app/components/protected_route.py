import reflex as rx
from app.states.auth_state import AuthState


def access_denied_message() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("shield-alert", class_name="w-16 h-16 text-red-500 mb-4"),
            rx.el.h1("Access Denied", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "You don't have permission to view this page.",
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


def loading_screen() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.spinner(size="3", class_name="text-[#6200EA] mb-4"),
            rx.el.p(
                "Verifying access...",
                class_name="text-gray-500 font-medium animate-pulse text-sm",
            ),
            class_name="flex flex-col items-center justify-center bg-white p-8 rounded-2xl shadow-lg border border-gray-100",
        ),
        class_name="fixed inset-0 bg-gray-50/90 backdrop-blur-sm flex items-center justify-center z-50",
    )


def protected_admin(component: rx.Component) -> rx.Component:
    """Restrict access to admin users only."""
    return rx.cond(
        AuthState.is_checking_auth,
        loading_screen(),
        rx.cond(AuthState.is_admin, component, access_denied_message()),
    )


def protected_shop_owner(component: rx.Component) -> rx.Component:
    """Restrict access to shop owners only."""
    return rx.cond(
        AuthState.is_checking_auth,
        loading_screen(),
        rx.cond(AuthState.is_shop_owner, component, access_denied_message()),
    )


def protected_rider(component: rx.Component) -> rx.Component:
    """Restrict access to riders only."""
    return rx.cond(
        AuthState.is_checking_auth,
        loading_screen(),
        rx.cond(
            AuthState.is_authenticated & AuthState.is_rider,
            component,
            access_denied_message(),
        ),
    )