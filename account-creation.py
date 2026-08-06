import re
import bcrypt
from typing import Dict, Optional
from pydantic import BaseModel, EmailStr, field_validator


# 1. In-memory Database Simulation (Replace with PostgreSQL/MongoDB in production)
user_database: Dict[str, dict] = {}


# 2. Request Data Validation Schema
class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit.")
        return password


# 3. Core Service Logic
class AuthService:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @classmethod
    def register_user(cls, user_data: UserRegisterSchema) -> dict:
        email = user_data.email.lower()

        # Check if account already exists
        if email in user_database:
            raise ValueError("An account with this email already exists.")

        # Hash password securely
        hashed_password = cls.hash_password(user_data.password)

        # Create user record
        user_record = {
            "email": email,
            "password_hash": hashed_password,
            "is_verified": False,  # Pending OTP/Email verification
        }

        # Save to DB
        user_database[email] = user_record

        return {
            "status": "success",
            "message": "User account created successfully.",
            "email": email,
        }


# Example Usage
if __name__ == "__main__":
    try:
        # Valid signup
        new_user = UserRegisterSchema(
            email="user@example.com", password="SecurePassword1"
        )
        result = AuthService.register_user(new_user)
        print("Success:", result)

        # Duplicate email test
        AuthService.register_user(new_user)
    except ValueError as e:
        print("Validation/Auth Error:", e)
