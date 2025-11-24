import reflex as rx
import logging
from app.pages.home import home_page
from app.pages.shops import shop_list_page
from app.pages.products import products_page
from app.pages.cart import cart_page
from app.pages.checkout import checkout_page
from app.pages.tracking import tracking_page
from app.pages.account import account_page
from app.states.main_state import AppState
from app.pages.shop_owner.dashboard import dashboard_page
from app.pages.shop_owner.products import products_page as owner_products_page
from app.pages.shop_owner.orders import orders_page
from app.pages.shop_owner.payouts import payouts_page
from app.states.shop_owner_state import ShopOwnerState
from app.pages.auth.login import login_page
from app.pages.auth.register import register_page
from app.states.auth_state import AuthState
from app.utils.db_seed import seed_database

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(home_page, route="/", on_load=[AuthState.check_auth, AppState.on_mount])
app.add_page(
    shop_list_page, route="/shops", on_load=[AuthState.check_auth, AppState.on_mount]
)
app.add_page(
    products_page,
    route="/shop/[id]",
    on_load=[AuthState.check_auth, AppState.on_mount, AppState.load_shop_page],
)
app.add_page(
    cart_page, route="/cart", on_load=[AuthState.check_auth, AppState.on_mount]
)
app.add_page(checkout_page, route="/checkout", on_load=AuthState.require_auth)
app.add_page(
    tracking_page,
    route="/tracking/[id]",
    on_load=[AuthState.check_auth, AppState.on_mount],
)
app.add_page(account_page, route="/account", on_load=AuthState.require_auth)
app.add_page(login_page, route="/login", on_load=AuthState.check_auth)
app.add_page(register_page, route="/register", on_load=AuthState.check_auth)
app.add_page(
    dashboard_page,
    route="/shop-owner/dashboard",
    on_load=[AuthState.check_auth, ShopOwnerState.on_mount],
)
app.add_page(
    owner_products_page,
    route="/shop-owner/products",
    on_load=[AuthState.check_auth, ShopOwnerState.on_mount],
)
app.add_page(
    orders_page,
    route="/shop-owner/orders",
    on_load=[AuthState.check_auth, ShopOwnerState.on_mount],
)
app.add_page(
    payouts_page,
    route="/shop-owner/payouts",
    on_load=[AuthState.check_auth, ShopOwnerState.on_mount],
)
from app.pages.rider.dashboard import dashboard_page as rider_dashboard
from app.pages.rider.orders import orders_page as rider_orders
from app.pages.rider.deliveries import deliveries_page as rider_deliveries
from app.pages.rider.earnings import earnings_page as rider_earnings
from app.states.rider_state import RiderState

app.add_page(
    rider_dashboard,
    route="/rider/dashboard",
    on_load=[AuthState.check_auth, RiderState.on_mount],
)
app.add_page(
    rider_orders,
    route="/rider/orders",
    on_load=[AuthState.check_auth, RiderState.on_mount],
)
app.add_page(
    rider_deliveries,
    route="/rider/deliveries",
    on_load=[AuthState.check_auth, RiderState.on_mount],
)
app.add_page(
    rider_earnings,
    route="/rider/earnings",
    on_load=[AuthState.check_auth, RiderState.on_mount],
)
from app.pages.admin.dashboard import dashboard_page as admin_dashboard
from app.pages.admin.shops import shops_page
from app.pages.admin.categories import categories_page
from app.pages.admin.orders import orders_page as admin_orders
from app.pages.admin.riders import riders_page
from app.pages.admin.pricing import pricing_page
from app.pages.admin.reports import reports_page
from app.states.admin_state import AdminState

app.add_page(
    admin_dashboard,
    route="/admin/dashboard",
    on_load=[AuthState.check_auth, AdminState.on_mount],
)
app.add_page(
    categories_page,
    route="/admin/categories",
    on_load=[AuthState.check_auth, AdminState.on_mount],
)
app.add_page(
    shops_page,
    route="/admin/shops",
    on_load=[AuthState.check_auth, AdminState.on_mount],
)
app.add_page(
    admin_orders,
    route="/admin/orders",
    on_load=[AuthState.check_auth, AdminState.on_mount],
)
app.add_page(
    riders_page,
    route="/admin/riders",
    on_load=[AuthState.check_auth, AdminState.on_mount],
)
app.add_page(
    pricing_page,
    route="/admin/pricing",
    on_load=[AuthState.check_auth, AdminState.on_mount],
)
app.add_page(
    reports_page,
    route="/admin/reports",
    on_load=[AuthState.check_auth, AdminState.on_mount],
)
try:
    seed_database()
except Exception as e:
    logging.exception(f"Database seeding skipped or failed: {e}")