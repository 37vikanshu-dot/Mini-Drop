import reflex as rx
from app.components.layout import layout
from app.states.main_state import AppState
from app.data import OrderItemDict


def cart_item(item: OrderItemDict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=item["image_url"], class_name="w-16 h-16 object-cover rounded-lg"
            ),
            rx.el.div(
                rx.el.h3(item["name"], class_name="text-sm font-bold text-gray-900"),
                rx.el.p(
                    f"₹{item['price']}", class_name="text-xs font-medium text-gray-500"
                ),
                class_name="ml-3 flex-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("minus", class_name="w-3 h-3"),
                    on_click=AppState.remove_from_cart(item["product_id"]),
                    class_name="w-7 h-7 flex items-center justify-center bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200",
                ),
                rx.el.span(
                    item["quantity"],
                    class_name="text-sm font-bold text-gray-900 w-6 text-center",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-3 h-3"),
                    on_click=AppState.add_to_cart(item["product_id"]),
                    class_name="w-7 h-7 flex items-center justify-center bg-[#6200EA] text-white rounded-lg hover:bg-[#5000CA]",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-center p-3",
        ),
        class_name="bg-white rounded-xl border border-gray-100 shadow-sm mb-3",
    )


def cart_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.h1("Your Cart", class_name="text-2xl font-bold text-gray-900 mb-6"),
            rx.cond(
                AppState.cart_count > 0,
                rx.el.div(
                    rx.el.div(
                        rx.foreach(AppState.cart_items_details, cart_item),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Bill Details",
                            class_name="text-sm font-bold text-gray-900 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "Item Total", class_name="text-sm text-gray-600"
                                ),
                                rx.el.span(
                                    f"₹{AppState.cart_total}",
                                    class_name="text-sm font-medium text-gray-900",
                                ),
                                class_name="flex justify-between mb-2",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Delivery Fee", class_name="text-sm text-gray-600"
                                ),
                                rx.el.span(
                                    f"₹{AppState.delivery_fee}",
                                    class_name="text-sm font-medium text-gray-900",
                                ),
                                class_name="flex justify-between mb-2",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Platform Fee", class_name="text-sm text-gray-600"
                                ),
                                rx.el.span(
                                    f"₹{AppState.platform_fee}",
                                    class_name="text-sm font-medium text-gray-900",
                                ),
                                class_name="flex justify-between mb-2",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "GST & Taxes", class_name="text-sm text-gray-600"
                                ),
                                rx.el.span(
                                    f"₹{AppState.tax_amount}",
                                    class_name="text-sm font-medium text-gray-900",
                                ),
                                class_name="flex justify-between mb-2",
                            ),
                            rx.cond(
                                AppState.applied_coupon,
                                rx.el.div(
                                    rx.el.span(
                                        "Coupon Discount",
                                        class_name="text-sm text-green-600",
                                    ),
                                    rx.el.span(
                                        f"-₹{AppState.coupon_discount_amount}",
                                        class_name="text-sm font-medium text-green-600",
                                    ),
                                    class_name="flex justify-between mb-2",
                                ),
                            ),
                            rx.el.div(class_name="h-px bg-gray-200 my-2"),
                            rx.el.div(
                                rx.el.span(
                                    "To Pay",
                                    class_name="text-base font-bold text-gray-900",
                                ),
                                rx.el.span(
                                    f"₹{AppState.cart_grand_total}",
                                    class_name="text-base font-bold text-[#6200EA]",
                                ),
                                class_name="flex justify-between",
                            ),
                            class_name="bg-white rounded-xl border border-gray-100 shadow-sm p-4 mb-6",
                        ),
                    ),
                    rx.cond(
                        AppState.applied_coupon,
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "tag", class_name="w-4 h-4 text-green-600 mr-2"
                                    ),
                                    rx.el.span(
                                        AppState.applied_coupon["code"],
                                        class_name="font-bold text-green-700 text-sm",
                                    ),
                                    class_name="flex items-center",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        f"-₹{AppState.coupon_discount_amount}",
                                        class_name="font-bold text-green-600 text-sm mr-3",
                                    ),
                                    rx.el.button(
                                        rx.icon("x", class_name="w-4 h-4"),
                                        on_click=AppState.remove_coupon,
                                        class_name="text-gray-400 hover:text-red-500 transition-colors",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="flex justify-between items-center bg-green-50 border border-green-200 rounded-xl p-3 mb-6",
                            )
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.input(
                                    placeholder="Enter promo code",
                                    on_change=AppState.set_promo_code_input,
                                    class_name="flex-1 bg-gray-50 border-none rounded-lg py-2.5 px-4 text-sm focus:ring-1 focus:ring-[#6200EA]",
                                    default_value=AppState.promo_code_input,
                                ),
                                rx.el.button(
                                    "Apply",
                                    on_click=AppState.apply_coupon,
                                    class_name="ml-3 px-4 py-2.5 bg-gray-900 text-white text-sm font-bold rounded-lg hover:bg-gray-800",
                                ),
                                class_name="flex",
                            ),
                            rx.cond(
                                AppState.coupon_error != "",
                                rx.el.p(
                                    AppState.coupon_error,
                                    class_name="text-xs text-red-500 mt-2 ml-1",
                                ),
                            ),
                            class_name="mb-8",
                        ),
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Proceed to Checkout",
                            class_name="w-full bg-[#6200EA] text-white py-3.5 rounded-xl font-bold shadow-lg hover:shadow-xl hover:bg-[#5000CA] transition-all active:scale-95",
                        ),
                        href="/checkout",
                    ),
                ),
                rx.el.div(
                    rx.icon("shopping-cart", class_name="w-16 h-16 text-gray-300 mb-4"),
                    rx.el.h3(
                        "Your cart is empty",
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Add items from shops to get started",
                        class_name="text-sm text-gray-500 mt-1 mb-6",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Browse Shops",
                            class_name="px-6 py-2.5 bg-[#6200EA] text-white rounded-full font-bold text-sm hover:bg-[#5000CA]",
                        ),
                        href="/shops",
                    ),
                    class_name="flex flex-col items-center justify-center py-16",
                ),
            ),
            class_name="max-w-2xl mx-auto px-4",
        )
    )