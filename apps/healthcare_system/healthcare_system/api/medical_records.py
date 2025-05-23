import frappe
from .jwt_auth import authenticate

@frappe.whitelist()
@authenticate()
def get_medical_records_by_patient(patient_id):
    return frappe.get_all(
        "Medical Record",
        filters={"patient": patient_id},
        fields=["name", "record_type", "notes", "diagnosis", "test_results", "appointment", "creation"]
    )

@frappe.whitelist()
@authenticate()
def get_prescriptions(record_id):
    record = frappe.get_doc("Medical Record", record_id)
    return record.prescriptions
