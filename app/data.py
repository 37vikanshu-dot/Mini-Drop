from typing import TypedDict
from app.utils.auth import hash_password


class CategoryDict(TypedDict):
    id: int
    name: str
    slug: str
    icon: str
    color_bg: str
    is_active: bool
    sort_order: int


class ShopDict(TypedDict):
    id: int
    name: str
    category_slug: str
    rating: float
    delivery_time: str
    distance: str
    image_url: str
    address: str
    is_featured: bool


class ProductDict(TypedDict):
    id: int
    shop_id: int
    name: str
    price: float
    original_price: float
    image_url: str
    description: str
    is_available: bool
    unit: str


class SavedAddressDict(TypedDict):
    id: str
    type: str
    address: str
    phone: str


class OrderItemDict(TypedDict):
    product_id: int
    name: str
    price: float
    quantity: int
    image_url: str


class OrderDict(TypedDict):
    id: str
    items: list[OrderItemDict]
    subtotal: float
    delivery_fee: float
    total_amount: float
    status: str
    date: str
    time: str
    delivery_address: str
    payment_method: str
    shop_id: int
    user_id: str


class WeeklyStatDict(TypedDict):
    day: str
    revenue: float
    orders: int


class PayoutDict(TypedDict):
    id: str
    date: str
    order_id: str
    order_amount: float
    commission: float
    payout_amount: float
    status: str


class RiderDict(TypedDict):
    id: str
    name: str
    phone: str
    vehicle_type: str
    status: str
    earnings: float
    completed_orders: int


class CouponDict(TypedDict):
    code: str
    discount: float
    type: str
    min_order: float
    is_active: bool


class UserDict(TypedDict):
    id: str
    name: str
    email: str
    phone: str
    role: str
    password_hash: str
    shop_id: int | None


USERS: list[UserDict] = [
    {
        "id": "user_001",
        "name": "Admin User",
        "email": "admin@minidrop.com",
        "phone": "9999999999",
        "role": "admin",
        "password_hash": hash_password("password123"),
        "shop_id": None,
    },
    {
        "id": "user_002",
        "name": "Shop Owner",
        "email": "owner@freshmart.com",
        "phone": "8888888888",
        "role": "shop_owner",
        "password_hash": hash_password("password123"),
        "shop_id": 1,
    },
    {
        "id": "user_003",
        "name": "John Doe",
        "email": "customer@example.com",
        "phone": "7777777777",
        "role": "customer",
        "password_hash": hash_password("password123"),
        "shop_id": None,
    },
    {
        "id": "rider_r1",
        "name": "Rahul Kumar",
        "email": "rahul@minidrop.com",
        "phone": "9876543210",
        "role": "rider",
        "password_hash": hash_password("password123"),
        "shop_id": None,
    },
]
CATEGORIES: list[CategoryDict] = [
    {
        "id": 1,
        "name": "Groceries",
        "slug": "grocery",
        "icon": "shopping-basket",
        "color_bg": "bg-green-100",
    },
    {
        "id": 2,
        "name": "Snacks",
        "slug": "snacks",
        "icon": "cookie",
        "color_bg": "bg-orange-100",
    },
    {
        "id": 3,
        "name": "Dairy",
        "slug": "dairy",
        "icon": "milk",
        "color_bg": "bg-blue-100",
    },
    {
        "id": 4,
        "name": "Medicines",
        "slug": "medical",
        "icon": "pill",
        "color_bg": "bg-red-100",
    },
    {
        "id": 5,
        "name": "Stationery",
        "slug": "stationery",
        "icon": "pencil",
        "color_bg": "bg-yellow-100",
    },
    {
        "id": 6,
        "name": "Bakery",
        "slug": "bakery",
        "icon": "croissant",
        "color_bg": "bg-amber-100",
    },
]
SHOPS: list[ShopDict] = [
    {
        "id": 1,
        "name": "Fresh Mart Grocery",
        "category_slug": "grocery",
        "rating": 4.8,
        "delivery_time": "15-20 min",
        "distance": "0.8 km",
        "image_url": "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=400&q=80",
        "address": "12 Main St",
        "is_featured": True,
    },
    {
        "id": 2,
        "name": "City Medicos",
        "category_slug": "medical",
        "rating": 4.5,
        "delivery_time": "10-15 min",
        "distance": "0.5 km",
        "image_url": "https://images.unsplash.com/photo-1585435557343-3b092031a831?auto=format&fit=crop&w=400&q=80",
        "address": "45 Park Ave",
        "is_featured": True,
    },
    {
        "id": 3,
        "name": "Daily Dairy Needs",
        "category_slug": "dairy",
        "rating": 4.9,
        "delivery_time": "10 min",
        "distance": "0.2 km",
        "image_url": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?auto=format&fit=crop&w=400&q=80",
        "address": "88 Market Rd",
        "is_featured": False,
    },
    {
        "id": 4,
        "name": "Student Stationers",
        "category_slug": "stationery",
        "rating": 4.2,
        "delivery_time": "25-30 min",
        "distance": "1.5 km",
        "image_url": "https://images.unsplash.com/photo-1550399105-c4db5fb85c18?auto=format&fit=crop&w=400&q=80",
        "address": "University Sq",
        "is_featured": False,
    },
    {
        "id": 5,
        "name": "Oven Fresh Bakery",
        "category_slug": "bakery",
        "rating": 4.7,
        "delivery_time": "20-25 min",
        "distance": "1.2 km",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&q=80",
        "address": "Baker St",
        "is_featured": True,
    },
]
PRODUCTS: list[ProductDict] = [
    {
        "id": 1,
        "shop_id": 1,
        "name": "Full Cream Milk",
        "price": 32.0,
        "original_price": 35.0,
        "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=200&q=80",
        "description": "Fresh full cream milk",
        "is_available": True,
        "unit": "1 L",
    },
    {
        "id": 2,
        "shop_id": 1,
        "name": "Whole Wheat Bread",
        "price": 45.0,
        "original_price": 50.0,
        "image_url": "https://images.unsplash.com/photo-1598373182133-52452f7691ef?auto=format&fit=crop&w=200&q=80",
        "description": "Freshly baked brown bread",
        "is_available": True,
        "unit": "400g",
    },
    {
        "id": 3,
        "shop_id": 1,
        "name": "Farm Eggs",
        "price": 65.0,
        "original_price": 75.0,
        "image_url": "https://images.unsplash.com/photo-1506976785307-8732e854ad03?auto=format&fit=crop&w=200&q=80",
        "description": "Pack of 6 fresh eggs",
        "is_available": True,
        "unit": "6 pcs",
    },
    {
        "id": 4,
        "shop_id": 1,
        "name": "Maggie Noodles",
        "price": 14.0,
        "original_price": 15.0,
        "image_url": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?auto=format&fit=crop&w=200&q=80",
        "description": "Instant noodles",
        "is_available": True,
        "unit": "70g",
    },
    {
        "id": 5,
        "shop_id": 2,
        "name": "Paracetamol 500mg",
        "price": 20.0,
        "original_price": 22.0,
        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=200&q=80",
        "description": "Fever reducer",
        "is_available": True,
        "unit": "Strip of 10",
    },
    {
        "id": 6,
        "shop_id": 2,
        "name": "Cotton Bandage",
        "price": 30.0,
        "original_price": 35.0,
        "image_url": "https://images.unsplash.com/photo-1583947215259-38e31be8751f?auto=format&fit=crop&w=200&q=80",
        "description": "Sterile bandage",
        "is_available": True,
        "unit": "1 Roll",
    },
    {
        "id": 7,
        "shop_id": 1,
        "name": "Lays Classic Salted",
        "price": 20.0,
        "original_price": 20.0,
        "image_url": "https://images.unsplash.com/photo-1566478919030-2609e87011bc?auto=format&fit=crop&w=200&q=80",
        "description": "Classic potato chips",
        "is_available": True,
        "unit": "50g",
    },
    {
        "id": 8,
        "shop_id": 4,
        "name": "Ballpoint Pen Blue",
        "price": 10.0,
        "original_price": 12.0,
        "image_url": "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?auto=format&fit=crop&w=200&q=80",
        "description": "Smooth writing pen",
        "is_available": True,
        "unit": "1 pc",
    },
    {
        "id": 9,
        "shop_id": 4,
        "name": "Spiral Notebook",
        "price": 55.0,
        "original_price": 60.0,
        "image_url": "https://images.unsplash.com/photo-1531346878377-a516a63156a5?auto=format&fit=crop&w=200&q=80",
        "description": "100 pages ruled",
        "is_available": True,
        "unit": "1 pc",
    },
]
RIDERS: list[RiderDict] = [
    {
        "id": "r1",
        "name": "Rahul Kumar",
        "phone": "9876543210",
        "vehicle_type": "Bike",
        "status": "Online",
        "earnings": 1250.0,
        "completed_orders": 45,
    },
    {
        "id": "r2",
        "name": "Amit Singh",
        "phone": "9876543211",
        "vehicle_type": "Scooter",
        "status": "Offline",
        "earnings": 890.0,
        "completed_orders": 32,
    },
]
COUPONS: list[CouponDict] = [
    {
        "code": "WELCOME50",
        "discount": 50.0,
        "type": "Flat",
        "min_order": 200.0,
        "is_active": True,
    },
    {
        "code": "FRESH20",
        "discount": 20.0,
        "type": "Percent",
        "min_order": 500.0,
        "is_active": True,
    },
]
ORDERS: list[OrderDict] = []