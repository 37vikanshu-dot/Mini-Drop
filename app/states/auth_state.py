import reflex as rx
from typing import Optional
from app.data import UserDict
import app.data as data
from app.utils.auth import hash_password, verify_password
from app.utils.supabase_client import get_supabase
import logging
from reflex_google_auth import GoogleAuthState
import uuid


class AuthState(GoogleAuthState):
    user_id_cookie: str = rx.Cookie(name="user_id")
    current_user: Optional[UserDict] = None
    user_role: str = "guest"
    is_checking_auth: bool = True
    login_email: str = ""
    login_password: str = ""
    error_message: str = ""
    register_name: str = ""
    register_email: str = ""
    register_phone: str = ""
    register_password: str = ""
    register_confirm_password: str = ""
    register_terms_accepted: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.current_user is not None

    @rx.var
    def is_admin(self) -> bool:
        return self.user_role == "admin"

    @rx.var
    def is_shop_owner(self) -> bool:
        return self.user_role == "shop_owner"

    @rx.var
    def is_rider(self) -> bool:
        return self.user_role == "rider"

    @rx.event
    def set_login_email(self, email: str):
        self.login_email = email

    @rx.event
    def set_login_password(self, password: str):
        self.login_password = password

    @rx.event
    def set_register_name(self, name: str):
        self.register_name = name

    @rx.event
    def set_register_email(self, email: str):
        self.register_email = email

    @rx.event
    def set_register_phone(self, phone: str):
        self.register_phone = phone

    @rx.event
    def set_register_password(self, password: str):
        self.register_password = password

    @rx.event
    def set_register_confirm_password(self, password: str):
        self.register_confirm_password = password

    @rx.event
    def toggle_register_terms(self, checked: bool):
        self.register_terms_accepted = checked

    @rx.event
    async def login(self):
        """Handle login form submission using Supabase."""
        self.is_checking_auth = True
        if not self.login_email or not self.login_password:
            self.error_message = "Please enter both email and password"
            self.is_checking_auth = False
            return
        supabase = get_supabase()
        if not supabase:
            user = next((u for u in data.USERS if u["email"] == self.login_email), None)
            if user and verify_password(self.login_password, user["password_hash"]):
                self.current_user = {
                    "id": str(user["id"]),
                    "name": user["name"],
                    "email": user["email"],
                    "phone": user["phone"],
                    "role": user["role"],
                    "password_hash": "",
                    "shop_id": user.get("shop_id"),
                }
                self.user_role = user["role"]
                self.user_id_cookie = str(user["id"])
                self.error_message = ""
                self.login_password = ""
                self.is_checking_auth = False
                return AuthState.redirect_based_on_role()
            self.error_message = "Invalid email or password"
            self.is_checking_auth = False
            return
        try:
            response = (
                supabase.table("users")
                .select("*")
                .eq("email", self.login_email)
                .execute()
            )
            users = response.data
            if not users:
                self.error_message = "Invalid email or password"
                self.is_checking_auth = False
                return
            user = users[0]
            if not verify_password(self.login_password, user["password_hash"]):
                self.error_message = "Invalid email or password"
                self.is_checking_auth = False
                return
            self.current_user = {
                "id": str(user["id"]),
                "name": user["name"],
                "email": user["email"],
                "phone": user.get("phone", ""),
                "role": user["role"],
                "password_hash": "",
                "shop_id": user.get("shop_id"),
            }
            self.user_role = user["role"]
            self.user_id_cookie = str(user["id"])
            self.error_message = ""
            self.login_password = ""
            self.is_checking_auth = False
            return AuthState.redirect_based_on_role()
        except Exception as e:
            logging.exception(f"Login error: {e}")
            self.error_message = "An error occurred during login"
            self.is_checking_auth = False

    @rx.event
    async def logout(self):
        """Handle logout."""
        self.current_user = None
        self.user_role = "guest"
        self.user_id_cookie = ""
        self.is_checking_auth = False
        return rx.redirect("/login")

    @rx.event
    async def register(self):
        """Handle registration using Supabase."""
        self.is_checking_auth = True
        if not self.register_terms_accepted:
            self.error_message = "You must accept the Terms & Conditions"
            self.is_checking_auth = False
            return
        if self.register_password != self.register_confirm_password:
            self.error_message = "Passwords do not match"
            self.is_checking_auth = False
            return
        supabase = get_supabase()
        if not supabase:
            existing_user = next(
                (u for u in data.USERS if u["email"] == self.register_email), None
            )
            if existing_user:
                self.error_message = "Email already registered"
                self.is_checking_auth = False
                return
            new_id = f"user_{len(data.USERS) + 100}"
            new_user = {
                "id": new_id,
                "name": self.register_name,
                "email": self.register_email,
                "phone": self.register_phone,
                "role": "customer",
                "password_hash": hash_password(self.register_password),
            }
            data.USERS.append(new_user)
            self.current_user = {
                "id": new_id,
                "name": self.register_name,
                "email": self.register_email,
                "phone": self.register_phone,
                "role": "customer",
                "password_hash": "",
                "shop_id": None,
            }
            self.user_role = "customer"
            self.user_id_cookie = new_id
            self.error_message = ""
            self.is_checking_auth = False
            return AuthState.redirect_based_on_role()
        try:
            response = (
                supabase.table("users")
                .select("email")
                .eq("email", self.register_email)
                .execute()
            )
            if response.data:
                self.error_message = "Email already registered"
                self.is_checking_auth = False
                return
            new_id = str(uuid.uuid4())
            hashed_pw = hash_password(self.register_password)
            new_user = {
                "id": new_id,
                "name": self.register_name,
                "email": self.register_email,
                "phone": self.register_phone,
                "role": "customer",
                "password_hash": hashed_pw,
            }
            supabase.table("users").insert(new_user).execute()
            self.current_user = {
                "id": new_id,
                "name": self.register_name,
                "email": self.register_email,
                "phone": self.register_phone,
                "role": "customer",
                "password_hash": "",
                "shop_id": None,
            }
            self.user_role = "customer"
            self.user_id_cookie = new_id
            self.error_message = ""
            self.register_password = ""
            self.register_confirm_password = ""
            self.is_checking_auth = False
            return AuthState.redirect_based_on_role()
        except Exception as e:
            logging.exception(f"Registration error: {e}")
            self.error_message = "Registration failed"
            self.is_checking_auth = False

    @rx.event
    async def check_auth(self):
        """Check authentication status on load."""
        self.is_checking_auth = True
        try:
            if self.token_is_valid:
                await self.sync_google_user()
                return
            if self.current_user:
                return
            if self.user_id_cookie:
                user_found = False
                supabase = get_supabase()
                if supabase:
                    try:
                        response = (
                            supabase.table("users")
                            .select("*")
                            .eq("id", self.user_id_cookie)
                            .execute()
                        )
                        if response.data:
                            user = response.data[0]
                            self.current_user = {
                                "id": str(user["id"]),
                                "name": user["name"],
                                "email": user["email"],
                                "phone": user.get("phone", ""),
                                "role": user["role"],
                                "password_hash": "",
                                "shop_id": user.get("shop_id"),
                            }
                            self.user_role = user["role"]
                            user_found = True
                    except Exception as e:
                        logging.exception(f"Error checking auth from Supabase: {e}")
                if not user_found:
                    user = next(
                        (u for u in data.USERS if str(u["id"]) == self.user_id_cookie),
                        None,
                    )
                    if user:
                        self.current_user = {
                            "id": str(user["id"]),
                            "name": user["name"],
                            "email": user["email"],
                            "phone": user.get("phone", ""),
                            "role": user["role"],
                            "password_hash": "",
                            "shop_id": user.get("shop_id"),
                        }
                        self.user_role = user["role"]
                        user_found = True
                if user_found:
                    return
            self.current_user = None
            self.user_role = "guest"
        except Exception as e:
            logging.exception(f"Error in check_auth: {e}")
            self.current_user = None
            self.user_role = "guest"
        finally:
            self.is_checking_auth = False

    @rx.event
    async def sync_google_user(self):
        """Sync Google User with Supabase Users table."""
        if not self.token_is_valid:
            return
        email = self.tokeninfo["email"]
        name = self.tokeninfo["name"]
        supabase = get_supabase()
        if not supabase:
            self.current_user = {
                "id": "google_user",
                "name": name,
                "email": email,
                "phone": "",
                "role": "customer",
                "password_hash": "",
                "shop_id": None,
            }
            self.user_role = "customer"
            self.user_id_cookie = "google_user"
            return
        try:
            res = supabase.table("users").select("*").eq("email", email).execute()
            if res.data:
                user = res.data[0]
            else:
                new_id = str(uuid.uuid4())
                new_user = {
                    "id": new_id,
                    "name": name,
                    "email": email,
                    "role": "customer",
                    "avatar_url": self.tokeninfo.get("picture", ""),
                    "password_hash": "",
                }
                supabase.table("users").insert(new_user).execute()
                user = new_user
            self.current_user = {
                "id": str(user["id"]),
                "name": user["name"],
                "email": user["email"],
                "phone": user.get("phone", ""),
                "role": user["role"],
                "password_hash": "",
                "shop_id": user.get("shop_id"),
            }
            self.user_role = user["role"]
            self.user_id_cookie = str(user["id"])
        except Exception as e:
            logging.exception(f"Error syncing Google user: {e}")

    @rx.event
    def require_auth(self):
        """Redirect to login if not authenticated."""
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    def redirect_based_on_role(self):
        if not self.current_user:
            return rx.redirect("/")
        role = self.current_user.get("role", "customer")
        if role == "admin":
            return rx.redirect("/admin/dashboard")
        elif role == "shop_owner":
            return rx.redirect("/shop-owner/dashboard")
        elif role == "rider":
            return rx.redirect("/rider/dashboard")
        else:
            return rx.redirect("/")