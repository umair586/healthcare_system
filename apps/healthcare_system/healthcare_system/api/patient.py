import frappe
from .jwt_auth import authenticate

@frappe.whitelist()
@authenticate()
def get_patient_profile(patient_id):
    return frappe.get_doc("Patient", patient_id).as_dict()


@frappe.whitelist()
@authenticate()
def search(query):
    return frappe.get_all("Patient", filters={"full_name": ["like", f"%{query}%"]}, fields=["name", "full_name"])

