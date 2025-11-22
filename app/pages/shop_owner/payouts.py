import reflex as rx
from app.components.shop_owner_layout import shop_owner_layout
from app.states.shop_owner_state import ShopOwnerState
from app.data import PayoutDict
from app.components.protected_route import protected_shop_owner


def payout_row(payout: PayoutDict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(payout["date"], class_name="text-sm font-medium text-gray-900"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(f"#{payout['order_id']}", class_name="text-sm text-gray-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"₹{payout['order_amount']}", class_name="text-sm text-gray-900"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(f"-₹{payout['commission']}", class_name="text-sm text-red-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"₹{payout['payout_amount']}",
                class_name="text-sm font-bold text-green-600",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                payout["status"],
                class_name="px-2 py-1 text-xs font-bold text-blue-700 bg-blue-100 rounded-full",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
    )


def payouts_page() -> rx.Component:
    return protected_shop_owner(
        shop_owner_layout(
            rx.el.div(
                rx.el.h1("Payouts", class_name="text-2xl font-bold text-gray-900 mb-6"),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Total Earnings",
                            class_name="text-sm font-medium text-white/80 mb-1",
                        ),
                        rx.el.p(
                            f"₹{ShopOwnerState.total_earnings}",
                            class_name="text-3xl font-bold text-white",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Withdraw",
                            class_name="bg-white text-[#6200EA] px-6 py-2 rounded-full font-bold text-sm shadow-lg hover:shadow-xl transition-all",
                        )
                    ),
                    class_name="bg-gradient-to-r from-[#6200EA] to-[#9046FC] p-8 rounded-2xl shadow-lg shadow-purple-200 flex justify-between items-center mb-8",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Transaction History",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Date",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Order ID",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Amount",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Commission",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Net Payout",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Status",
                                        class_name="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                ),
                                class_name="bg-gray-50 border-b border-gray-100",
                            ),
                            rx.el.tbody(
                                rx.foreach(ShopOwnerState.payouts, payout_row),
                                class_name="bg-white divide-y divide-gray-100",
                            ),
                            class_name="min-w-full",
                        ),
                        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
                    ),
                ),
            )
        )
    )