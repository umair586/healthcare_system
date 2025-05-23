import functools
import frappe
import jwt
from datetime import datetime, timedelta

SECRET_KEY = frappe.conf.jwt_secret or "secret"
EXPIRY_MINUTES = 60

def generate_jwt(user):
    payload = {
        "user": user,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRY_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        frappe.throw("Token expired", frappe.AuthenticationError)
    except jwt.InvalidTokenError:
        frappe.throw("Invalid token", frappe.AuthenticationError)


def authenticate(allowed_roles=None):
    """Restrict access to users having certain roles."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = frappe.get_request_header("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                frappe.throw("Missing or invalid Authorization header", frappe.AuthenticationError)

            token = auth_header.split(" ")[1]
            payload = decode_jwt(token)

            frappe.local.jwt_user = payload["user"]

            if allowed_roles:
                user_roles = frappe.get_roles(payload["user"])
                if not set(user_roles).intersection(set(allowed_roles)):
                    frappe.throw("Access denied: Insufficient role", frappe.PermissionError)

            return func(*args, **kwargs)
        return wrapper
    return decorator
