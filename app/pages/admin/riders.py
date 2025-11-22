import reflex as rx
from app.components.admin_layout import admin_layout
from app.states.admin_state import AdminState
from app.data import RiderDict
from app.components.protected_route import protected_admin


def rider_row(rider: RiderDict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        rider["name"], class_name="text-sm font-bold text-gray-900"
                    ),
                    rx.el.p(rider["phone"], class_name="text-xs text-gray-500"),
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                rider["vehicle_type"], class_name="text-sm font-medium text-gray-600"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"₹{rider['earnings']}", class_name="text-sm font-bold text-green-600"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                rider["completed_orders"],
                class_name="text-sm font-medium text-gray-900",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                rx.cond(
                    rider["status"] == "Online",
                    rx.el.span(
                        "Online",
                        class_name="px-2 py-1 text-xs font-bold text-green-700 bg-green-100 rounded-full",
                    ),
                    rx.el.span(
                        "Offline",
                        class_name="px-2 py-1 text-xs font-bold text-gray-600 bg-gray-100 rounded-full",
                    ),
                ),
                on_click=AdminState.toggle_rider_status(rider["id"]),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
    )


def rider_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Add Delivery Partner",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Full Name",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="Enter rider name",
                            on_change=AdminState.set_rider_form_name,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Phone Number",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="Enter phone number",
                            on_change=AdminState.set_rider_form_phone,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Vehicle Type",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Bike", value="Bike"),
                            rx.el.option("Scooter", value="Scooter"),
                            rx.el.option("Cycle", value="Cycle"),
                            on_change=AdminState.set_rider_form_vehicle,
                            class_name="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-[#6200EA] focus:border-[#6200EA] mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                class_name="px-4 py-2 text-sm font-bold text-gray-600 hover:bg-gray-100 rounded-lg mr-2",
                            )
                        ),
                        rx.el.button(
                            "Add Rider",
                            on_click=AdminState.save_rider,
                            class_name="px-4 py-2 bg-[#6200EA] text-white text-sm font-bold rounded-lg hover:bg-[#5000CA]",
                        ),
                        class_name="flex justify-end",
                    ),
                ),
                class_name="fixed left-[50%] top-[50%] z-50 max-h-[85vh] w-[90vw] max-w-md translate-x-[-50%] translate-y-[-50%] bg-white rounded-2xl p-6 shadow-2xl focus:outline-none",
            ),
        ),
        open=AdminState.is_rider_dialog_open,
        on_open_change=AdminState.set_rider_dialog_open,
    )


def riders_page() -> rx.Component:
    return protected_admin(
        admin_layout(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Delivery Partners",
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-4 h-4 mr-2"),
                        "Add Rider",
                        on_click=AdminState.open_add_rider_dialog,
                        class_name="flex items-center px-4 py-2 bg-[#6200EA] text-white rounded-xl font-bold text-sm hover:bg-[#5000CA] shadow-sm hover:shadow-md transition-all",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Rider Details",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Vehicle",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Earnings",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Orders",
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
                            rx.foreach(AdminState.riders, rider_row),
                            class_name="bg-white divide-y divide-gray-100",
                        ),
                        class_name="min-w-full",
                    ),
                    class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
                ),
                rider_dialog(),
            )
        )
    )