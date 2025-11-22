-- ============================================================
-- Mini Drop - Hyperlocal Delivery Platform Database Schema
-- ============================================================
-- This file creates all required tables and inserts sample data
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard
-- ============================================================

-- ============================================================
-- STEP 1: CREATE TABLES
-- ============================================================

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    role TEXT DEFAULT 'customer',
    password_hash TEXT NOT NULL,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    icon TEXT,
    color_bg TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0
);

-- Create shops table
CREATE TABLE IF NOT EXISTS shops (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_slug TEXT,
    rating DECIMAL(2,1) DEFAULT 5.0,
    delivery_time TEXT,
    distance TEXT,
    image_url TEXT,
    address TEXT,
    is_featured BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    shop_id INTEGER REFERENCES shops(id),
    name TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2),
    image_url TEXT,
    description TEXT,
    is_available BOOLEAN DEFAULT TRUE,
    unit TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    subtotal DECIMAL(10,2) NOT NULL,
    delivery_fee DECIMAL(10,2) DEFAULT 15.0,
    total_amount DECIMAL(10,2) NOT NULL,
    status TEXT DEFAULT 'Pending',
    date TEXT,
    time TEXT,
    delivery_address TEXT,
    payment_method TEXT,
    shop_id INTEGER REFERENCES shops(id),
    user_id TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id TEXT REFERENCES orders(id),
    product_id INTEGER,
    name TEXT,
    price DECIMAL(10,2),
    quantity INTEGER,
    image_url TEXT
);

-- Create riders table
CREATE TABLE IF NOT EXISTS riders (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    vehicle_type TEXT,
    status TEXT DEFAULT 'Offline',
    earnings DECIMAL(10,2) DEFAULT 0,
    completed_orders INTEGER DEFAULT 0
);

-- Create coupons table
CREATE TABLE IF NOT EXISTS coupons (
    code TEXT PRIMARY KEY,
    discount DECIMAL(10,2),
    type TEXT,
    min_order DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create addresses table
CREATE TABLE IF NOT EXISTS addresses (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    type TEXT,
    address TEXT,
    phone TEXT
);

-- Create payouts table
CREATE TABLE IF NOT EXISTS payouts (
    id TEXT PRIMARY KEY,
    date TEXT,
    order_id TEXT,
    order_amount DECIMAL(10,2),
    commission DECIMAL(10,2),
    payout_amount DECIMAL(10,2),
    status TEXT
);

-- ============================================================
-- STEP 2: INSERT SAMPLE DATA
-- ============================================================

-- Insert Users (password for all: password123)
INSERT INTO users (id, name, email, phone, role, password_hash) VALUES
('user_001', 'Admin User', 'admin@minidrop.com', '9999999999', 'admin', '$2b$12$aUj9a/s.iL.YOXA2eS9zAuQv4Y0WwmkbMjWQsfF92KuBaN/dC/uw6'),
('user_002', 'Shop Owner', 'owner@freshmart.com', '8888888888', 'shop_owner', '$2b$12$gAX9bshUNxx5iNLZcNJstuQCCt.4SkIyZfb.WoDnjGxlNj9eapJ1S'),
('user_003', 'John Doe', 'customer@example.com', '7777777777', 'customer', '$2b$12$RR44h7OlXPFR6V.IrSRC2enhLCuIYdvQTUyKnBpVnHneNxMUJN6lC')
ON CONFLICT (email) DO NOTHING;

-- Insert Categories
INSERT INTO categories (name, slug, icon, color_bg, sort_order) VALUES
('Groceries', 'grocery', 'shopping-basket', 'bg-green-100', 1),
('Snacks', 'snacks', 'cookie', 'bg-orange-100', 2),
('Dairy', 'dairy', 'milk', 'bg-blue-100', 3),
('Medicines', 'medical', 'pill', 'bg-red-100', 4),
('Stationery', 'stationery', 'pencil', 'bg-yellow-100', 5),
('Bakery', 'bakery', 'croissant', 'bg-amber-100', 6)
ON CONFLICT (slug) DO NOTHING;

-- Insert Shops
INSERT INTO shops (name, category_slug, rating, delivery_time, distance, image_url, address, is_featured) VALUES
('Fresh Mart Grocery', 'grocery', 4.8, '15-20 min', '0.8 km', 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=400&q=80', '12 Main St', TRUE),
('City Medicos', 'medical', 4.5, '10-15 min', '0.5 km', 'https://images.unsplash.com/photo-1585435557343-3b092031a831?auto=format&fit=crop&w=400&q=80', '45 Park Ave', TRUE),
('Daily Dairy Needs', 'dairy', 4.9, '10 min', '0.2 km', 'https://images.unsplash.com/photo-1628088062854-d1870b4553da?auto=format&fit=crop&w=400&q=80', '88 Market Rd', FALSE),
('Student Stationers', 'stationery', 4.2, '25-30 min', '1.5 km', 'https://images.unsplash.com/photo-1550399105-c4db5fb85c18?auto=format&fit=crop&w=400&q=80', 'University Sq', FALSE),
('Oven Fresh Bakery', 'bakery', 4.7, '20-25 min', '1.2 km', 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&q=80', 'Baker St', TRUE);

-- Insert Products (shop_id references the shops created above)
INSERT INTO products (shop_id, name, price, original_price, image_url, description, unit) VALUES
(1, 'Full Cream Milk', 32.00, 35.00, 'https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=200&q=80', 'Fresh full cream milk', '1 L'),
(1, 'Whole Wheat Bread', 45.00, 50.00, 'https://images.unsplash.com/photo-1598373182133-52452f7691ef?auto=format&fit=crop&w=200&q=80', 'Freshly baked brown bread', '400g'),
(1, 'Farm Eggs', 65.00, 75.00, 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?auto=format&fit=crop&w=200&q=80', 'Pack of 6 fresh eggs', '6 pcs'),
(1, 'Maggie Noodles', 14.00, 15.00, 'https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?auto=format&fit=crop&w=200&q=80', 'Instant noodles', '70g'),
(2, 'Paracetamol 500mg', 20.00, 22.00, 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=200&q=80', 'Fever reducer', 'Strip of 10'),
(2, 'Cotton Bandage', 30.00, 35.00, 'https://images.unsplash.com/photo-1583947215259-38e31be8751f?auto=format&fit=crop&w=200&q=80', 'Sterile bandage', '1 Roll'),
(1, 'Lays Classic Salted', 20.00, 20.00, 'https://images.unsplash.com/photo-1566478919030-2609e87011bc?auto=format&fit=crop&w=200&q=80', 'Classic potato chips', '50g'),
(4, 'Ballpoint Pen Blue', 10.00, 12.00, 'https://images.unsplash.com/photo-1585336261022-680e295ce3fe?auto=format&fit=crop&w=200&q=80', 'Smooth writing pen', '1 pc'),
(4, 'Spiral Notebook', 55.00, 60.00, 'https://images.unsplash.com/photo-1531346878377-a516a63156a5?auto=format&fit=crop&w=200&q=80', '100 pages ruled', '1 pc');

-- Insert Riders
INSERT INTO riders (id, name, phone, vehicle_type, status, earnings, completed_orders) VALUES
('r1', 'Rahul Kumar', '9876543210', 'Bike', 'Online', 1250.00, 45),
('r2', 'Amit Singh', '9876543211', 'Scooter', 'Offline', 890.00, 32)
ON CONFLICT (id) DO NOTHING;

-- Insert Coupons
INSERT INTO coupons (code, discount, type, min_order, is_active) VALUES
('WELCOME50', 50.00, 'Flat', 200.00, TRUE),
('FRESH20', 20.00, 'Percent', 500.00, TRUE)
ON CONFLICT (code) DO NOTHING;

-- ============================================================
-- STEP 3: VERIFY DATA
-- ============================================================
-- Run these queries to verify everything was created:
-- SELECT * FROM users;
-- SELECT * FROM categories;
-- SELECT * FROM shops;
-- SELECT * FROM products;
-- SELECT * FROM riders;
-- SELECT * FROM coupons;

-- ============================================================
-- LOGIN CREDENTIALS (password: password123)
-- ============================================================
-- Admin: admin@minidrop.com
-- Shop Owner: owner@freshmart.com
-- Customer: customer@example.com
-- ============================================================
