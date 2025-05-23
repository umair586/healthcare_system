import frappe
from .jwt_auth import authenticate

@frappe.whitelist()
@authenticate()
def get_patient_dashboard(patient_id):

    patient = frappe.get_value("Patient", patient_id, "name")
    if not patient:
        frappe.throw("No patient found")

    appointments = frappe.get_all("Appointment", filters={"patient": patient},
        fields=["name", "date", "time", "status", "doctor"],
        order_by="date desc", limit_page_length=5)

    records = frappe.get_all("Medical Record", filters={"patient": patient},
        fields=["name", "record_type", "diagnosis", "appointment", "modified"],
        order_by="modified desc", limit_page_length=5)

    return {
        "patient": patient,
        "appointments": appointments,
        "medical_records": records
    }
    
    
@frappe.whitelist()
@authenticate()
def get_appointments(patient_id):
    patient = frappe.get_value("Patient", patient_id, "name")
    if not patient:
        frappe.throw("Patient not found")

    return frappe.get_all("Appointment", filters={"patient": patient},
        fields=["name", "date", "time", "status", "doctor"], order_by="date desc")


@frappe.whitelist()
@authenticate()
def get_medical_records(patient_id):
    patient = frappe.get_value("Patient", patient_id, "name")
    if not patient:
        frappe.throw("Patient not found")

    return frappe.get_all("Medical Record", filters={"patient": patient},
        fields=["name", "record_type", "diagnosis", "appointment", "modified"],
        order_by="modified desc")

