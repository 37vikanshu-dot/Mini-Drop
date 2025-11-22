import reflex as rx
from app.components.admin_layout import admin_layout
from app.states.admin_state import AdminState
from app.components.protected_route import protected_admin


def pricing_page() -> rx.Component:
    return protected_admin(
        admin_layout(
            rx.el.div(
                rx.el.h1(
                    "Pricing & Commission",
                    class_name="text-2xl font-bold text-gray-900 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Delivery Charges",
                            class_name="text-lg font-bold text-gray-900 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Base Delivery Fee (₹)",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    on_change=AdminState.update_delivery_base,
                                    type="number",
                                    class_name="w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-[#6200EA] focus:border-[#6200EA]",
                                    default_value=AdminState.pricing_config[
                                        "delivery_base"
                                    ],
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Surge Multiplier (x)",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    on_change=AdminState.update_surge_multiplier,
                                    type="number",
                                    step="0.1",
                                    class_name="w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-[#6200EA] focus:border-[#6200EA]",
                                    default_value=AdminState.pricing_config[
                                        "surge_multiplier"
                                    ],
                                ),
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-6",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Active Coupons",
                            class_name="text-lg font-bold text-gray-900 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                AdminState.coupons,
                                lambda coupon: rx.el.div(
                                    rx.el.div(
                                        rx.el.p(
                                            coupon["code"],
                                            class_name="font-bold text-[#6200EA] text-lg",
                                        ),
                                        rx.el.p(
                                            f"{coupon['type']} Discount: {coupon['discount']}",
                                            class_name="text-sm text-gray-600",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            "Active",
                                            class_name="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-bold",
                                        )
                                    ),
                                    class_name="flex justify-between items-center p-4 border border-gray-200 rounded-xl mb-2",
                                ),
                            )
                        ),
                        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
                    ),
                ),
            )
        )
    )