import reflex as rx
from app.components.admin_layout import admin_layout
from app.states.admin_state import AdminState
from app.states.auth_state import AuthState
from app.states.ai_state import AIState


def loading_screen() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.spinner(size="3", class_name="text-[#6200EA] mb-4"),
            rx.el.p(
                "Loading dashboard...",
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


def stat_card(
    title: str, value: str, icon: str, trend: str, trend_up: bool
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
            ),
            rx.el.div(
                rx.icon(icon, class_name="w-6 h-6 text-[#6200EA]"),
                class_name="w-12 h-12 bg-purple-50 rounded-xl flex items-center justify-center",
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.icon(
                rx.cond(trend_up, "trending-up", "trending-down"),
                class_name=f"w-4 h-4 {rx.cond(trend_up, 'text-green-500', 'text-red-500')}",
            ),
            rx.el.span(
                trend,
                class_name=f"text-xs font-bold {rx.cond(trend_up, 'text-green-500', 'text-red-500')} ml-1",
            ),
            rx.el.span("vs last week", class_name="text-xs text-gray-400 ml-1"),
            class_name="flex items-center",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm",
    )


def ai_insight_card(title: str, content: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="w-5 h-5 text-[#6200EA] mb-2"),
            rx.el.h4(title, class_name="text-sm font-bold text-gray-900 mb-1"),
            rx.el.p(content, class_name="text-xs text-gray-600 leading-relaxed"),
            class_name="p-4 bg-gray-50 rounded-xl border border-gray-100 h-full",
        ),
        class_name="h-full",
    )


def dashboard_content() -> rx.Component:
    return admin_layout(
        rx.el.div(
            rx.el.h1(
                "Admin Dashboard", class_name="text-2xl font-bold text-gray-900 mb-6"
            ),
            rx.el.div(
                stat_card(
                    "Total Earnings",
                    f"₹{AdminState.total_earnings}",
                    "wallet",
                    "+15.3%",
                    True,
                ),
                stat_card(
                    "Orders Today",
                    AdminState.total_orders_today.to_string(),
                    "shopping-cart",
                    "+8.2%",
                    True,
                ),
                stat_card(
                    "Active Shops", f"{AdminState.shops.length()}", "store", "+2", True
                ),
                stat_card(
                    "Online Riders",
                    AdminState.active_riders_count.to_string(),
                    "bike",
                    "-1",
                    False,
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "AI Business Insights",
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.el.button(
                            rx.cond(
                                AIState.is_loading_insights,
                                rx.spinner(size="1", class_name="text-white"),
                                rx.icon("sparkles", class_name="w-4 h-4 text-white"),
                            ),
                            "Generate Insights",
                            on_click=AIState.generate_admin_insights,
                            disabled=AIState.is_loading_insights,
                            class_name="flex items-center gap-2 bg-[#6200EA] px-3 py-1.5 rounded-lg text-xs font-bold text-white hover:bg-[#5000CA] shadow-sm",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.cond(
                        AIState.admin_insights,
                        rx.el.div(
                            ai_insight_card(
                                "Demand Prediction",
                                AIState.admin_insights.demand_prediction,
                                "trending-up",
                            ),
                            ai_insight_card(
                                "Top Selling",
                                AIState.admin_insights.top_selling_analysis,
                                "award",
                            ),
                            ai_insight_card(
                                "Risk Analysis",
                                AIState.admin_insights.stock_risks.join(", "),
                                "flag_triangle_right",
                            ),
                            ai_insight_card(
                                "Peak Hours",
                                AIState.admin_insights.peak_hour_analysis,
                                "clock",
                            ),
                            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Click generate to analyze your platform data with AI.",
                                class_name="text-gray-500 text-sm text-center py-8",
                            ),
                            class_name="bg-gray-50 rounded-2xl border border-dashed border-gray-200",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mb-8",
                )
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Platform Revenue",
                        class_name="text-lg font-bold text-gray-900 mb-6",
                    ),
                    rx.el.div(
                        rx.recharts.area_chart(
                            rx.recharts.cartesian_grid(
                                horizontal=True, vertical=False, class_name="opacity-25"
                            ),
                            rx.recharts.graphing_tooltip(),
                            rx.recharts.area(
                                data_key="revenue",
                                stroke="#6200EA",
                                fill="#6200EA",
                                fill_opacity=0.1,
                                type_="monotone",
                                stroke_width=3,
                            ),
                            rx.recharts.x_axis(
                                data_key="day",
                                axis_line=False,
                                tick_line=False,
                                tick_size=10,
                                custom_attrs={"fontSize": "12px"},
                            ),
                            rx.recharts.y_axis(
                                axis_line=False,
                                tick_line=False,
                                tick_size=10,
                                custom_attrs={"fontSize": "12px"},
                            ),
                            data=AdminState.revenue_stats,
                            width="100%",
                            height=300,
                        ),
                        class_name="w-full",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex-1",
                ),
                class_name="flex mb-8",
            ),
        )
    )


from app.components.protected_route import protected_admin


def dashboard_page() -> rx.Component:
    return protected_admin(dashboard_content())