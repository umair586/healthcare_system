import frappe
from .jwt_auth import authenticate

@frappe.whitelist()
@authenticate()
def get_availability(doctor):
    return frappe.get_all(
        "Doctor Availability",
        filters={"parent": doctor},
        fields=["day", "start_time", "end_time"]
    )


@frappe.whitelist()
@authenticate()
def get_doctors_by_speciality(speciality):
    return frappe.get_all("Doctor", filters={"specialization": ["like", f"%{speciality}%"]}, fields=["name", "doctor_name", "department"])
