import reflex as rx
from app.components.admin_layout import admin_layout
from app.states.admin_state import AdminState
from app.components.protected_route import protected_admin


def reports_page() -> rx.Component:
    return protected_admin(
        admin_layout(
            rx.el.div(
                rx.el.h1(
                    "Analytics & Reports",
                    class_name="text-2xl font-bold text-gray-900 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Revenue Trend",
                            class_name="text-lg font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            rx.recharts.bar_chart(
                                rx.recharts.cartesian_grid(
                                    horizontal=True,
                                    vertical=False,
                                    class_name="opacity-25",
                                ),
                                rx.recharts.graphing_tooltip(),
                                rx.recharts.bar(
                                    data_key="revenue",
                                    fill="#6200EA",
                                    radius=[4, 4, 0, 0],
                                    bar_size=40,
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
                        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-6",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Orders Volume",
                            class_name="text-lg font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            rx.recharts.line_chart(
                                rx.recharts.cartesian_grid(
                                    horizontal=True,
                                    vertical=False,
                                    class_name="opacity-25",
                                ),
                                rx.recharts.graphing_tooltip(),
                                rx.recharts.line(
                                    data_key="orders",
                                    stroke="#00C853",
                                    stroke_width=3,
                                    type_="monotone",
                                    dot=True,
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
                        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
                    ),
                ),
            )
        )
    )