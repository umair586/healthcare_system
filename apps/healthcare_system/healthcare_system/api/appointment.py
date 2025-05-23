
import frappe
from .jwt_auth import authenticate

@frappe.whitelist()
@authenticate()
def check_availability(doctor, date, time):
    exists = frappe.db.exists("Appointment", {
        "doctor": doctor,
        "date": date,
        "time": time,
        "status": ["not in", ["Cancelled"]]
    })
    return not exists


@frappe.whitelist()
@authenticate()
def get_upcoming(patient):
    return frappe.get_all("Appointment", filters={
        "patient": patient,
        "date": [">=", frappe.utils.today()],
        "status": ["not in", ["Cancelled", "Completed"]]
    }, fields=["name", "date", "time", "doctor", "status"])
    
