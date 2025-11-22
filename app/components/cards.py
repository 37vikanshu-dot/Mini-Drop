import reflex as rx
from app.data import ShopDict, ProductDict, CategoryDict
from app.states.main_state import AppState


def category_card(category: CategoryDict) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.icon(category["icon"], class_name="w-6 h-6 text-gray-700"),
                class_name=f"w-12 h-12 {category['color_bg']} rounded-full flex items-center justify-center mb-2",
            ),
            rx.el.span(
                category["name"],
                class_name="text-xs font-medium text-center text-gray-700",
            ),
            class_name="flex flex-col items-center p-2 transition-transform hover:scale-105 cursor-pointer",
        ),
        href="/shops",
        on_click=lambda: AppState.set_category_filter(category["slug"]),
    )


def shop_card(shop: ShopDict) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.image(
                src=shop["image_url"], class_name="w-24 h-24 object-cover rounded-lg"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        shop["name"],
                        class_name="text-lg font-bold text-gray-900 leading-tight mb-1",
                    ),
                    rx.cond(
                        shop["is_featured"],
                        rx.el.span(
                            "Featured",
                            class_name="text-[10px] font-bold tracking-wider uppercase text-[#6200EA] bg-purple-50 px-2 py-0.5 rounded-full w-fit mb-1",
                        ),
                        None,
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "star", class_name="w-3 h-3 text-yellow-400 fill-yellow-400"
                        ),
                        rx.el.span(shop["rating"], class_name="text-xs font-bold ml-1"),
                        class_name="flex items-center",
                    ),
                    rx.el.div(class_name="w-1 h-1 rounded-full bg-gray-300 mx-2"),
                    rx.el.span(
                        shop["delivery_time"], class_name="text-xs text-gray-500"
                    ),
                    rx.el.div(class_name="w-1 h-1 rounded-full bg-gray-300 mx-2"),
                    rx.el.span(shop["distance"], class_name="text-xs text-gray-500"),
                    class_name="flex items-center mt-1",
                ),
                rx.el.p(
                    shop["address"], class_name="text-xs text-gray-400 mt-2 truncate"
                ),
                class_name="flex flex-col justify-center flex-1 ml-4",
            ),
            class_name="flex p-3",
        ),
        href=f"/shop/{shop['id']}",
        class_name="block bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-all duration-300 cursor-pointer mb-3",
    )


def product_card(product: ProductDict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=product["image_url"],
                class_name="w-full h-32 object-cover rounded-xl mb-3",
            ),
            rx.el.div(
                rx.el.h3(
                    product["name"],
                    class_name="text-sm font-bold text-gray-900 mb-1 truncate",
                ),
                rx.el.p(product["unit"], class_name="text-xs text-gray-400 mb-2"),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            f"₹{product['price']}",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        rx.el.span(
                            f"₹{product['original_price']}",
                            class_name="text-xs text-gray-400 line-through ml-2",
                        ),
                        class_name="flex items-baseline",
                    ),
                    rx.cond(
                        AppState.cart.contains(product["id"].to_string()),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("minus", class_name="w-3 h-3"),
                                on_click=AppState.remove_from_cart(product["id"]),
                                class_name="w-7 h-7 flex items-center justify-center bg-purple-100 text-[#6200EA] rounded-lg hover:bg-purple-200",
                            ),
                            rx.el.span(
                                AppState.cart[product["id"].to_string()],
                                class_name="text-sm font-bold text-[#6200EA] w-6 text-center",
                            ),
                            rx.el.button(
                                rx.icon("plus", class_name="w-3 h-3"),
                                on_click=AppState.add_to_cart(product["id"]),
                                class_name="w-7 h-7 flex items-center justify-center bg-[#6200EA] text-white rounded-lg hover:bg-[#5000CA]",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.el.button(
                            "ADD",
                            on_click=AppState.add_to_cart(product["id"]),
                            class_name="px-4 py-1.5 bg-white border border-[#6200EA] text-[#6200EA] text-xs font-bold rounded-lg hover:bg-[#6200EA] hover:text-white transition-all shadow-sm",
                        ),
                    ),
                    class_name="flex items-center justify-between mt-2",
                ),
                class_name="flex flex-col",
            ),
            class_name="p-2",
        ),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-all duration-300",
    )


def quick_item_card(product: ProductDict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=product["image_url"],
                class_name="w-16 h-16 object-cover rounded-lg mb-2",
            ),
            rx.el.p(
                product["name"],
                class_name="text-xs font-medium text-gray-800 truncate w-full text-center",
            ),
            class_name="flex flex-col items-center p-2",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-100 min-w-[100px] mr-3",
    )