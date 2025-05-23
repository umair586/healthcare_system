import frappe
from .jwt_auth import generate_jwt

@frappe.whitelist(allow_guest=True)
def login(email, password):
    from frappe.auth import LoginManager

    try:
        login_manager = LoginManager()
        login_manager.authenticate(email, password)
        login_manager.post_login()

        token = generate_jwt(email)
        return {"token": token, "user": email}
    except frappe.AuthenticationError:
        frappe.throw("Invalid credentials", frappe.AuthenticationError)
