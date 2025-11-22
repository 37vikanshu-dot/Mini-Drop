import reflex as rx
from app.components.shop_owner_layout import shop_owner_layout
from app.states.shop_owner_state import ShopOwnerState
from app.components.protected_route import protected_shop_owner


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


def create_gradient(color: str) -> rx.Component:
    id_safe = color.replace("#", "")
    return rx.el.svg.defs(
        rx.el.svg.linear_gradient(
            rx.el.svg.stop(stop_color=color, offset="5%", stop_opacity=0.3),
            rx.el.svg.stop(stop_color=color, offset="95%", stop_opacity=0),
            x1=0,
            x2=0,
            y1=0,
            y2=1,
            id=f"color{id_safe}",
        )
    )


def dashboard_page() -> rx.Component:
    return protected_shop_owner(
        shop_owner_layout(
            rx.el.div(
                rx.el.h1(
                    "Dashboard", class_name="text-2xl font-bold text-gray-900 mb-6"
                ),
                rx.el.div(
                    stat_card(
                        "Total Revenue",
                        f"₹{ShopOwnerState.total_revenue_today}",
                        "indian-rupee",
                        "+12.5%",
                        True,
                    ),
                    stat_card(
                        "Orders Today",
                        ShopOwnerState.total_orders_today,
                        "shopping-bag",
                        "+8.2%",
                        True,
                    ),
                    stat_card(
                        "Avg. Order Value", "₹340", "bar-chart-3", "-2.1%", False
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Weekly Revenue",
                            class_name="text-lg font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            rx.recharts.area_chart(
                                rx.recharts.cartesian_grid(
                                    horizontal=True,
                                    vertical=False,
                                    class_name="opacity-25",
                                ),
                                rx.recharts.graphing_tooltip(),
                                create_gradient("#6200EA"),
                                rx.recharts.area(
                                    data_key="revenue",
                                    stroke="#6200EA",
                                    fill="url(#color6200EA)",
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
                                data=ShopOwnerState.weekly_stats,
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
    )