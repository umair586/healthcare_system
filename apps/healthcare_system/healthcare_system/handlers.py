import frappe
from frappe.utils.password import update_password

def create_portal_user(doc, method):
    if not frappe.db.exists("User", doc.email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": doc.email,
            "first_name": doc.full_name,
            "send_welcome_email": 1,
            "role_profile_name": "Patient",
            "user_type": "Website User",
            "enabled": 1,
        })
        user.insert(ignore_permissions=True)
        frappe.db.commit()
        
        # Set default password (you can generate or hardcode)
        default_password = user.email
        update_password(user.name, default_password)