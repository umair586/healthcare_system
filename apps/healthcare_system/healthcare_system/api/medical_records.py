import frappe

@frappe.whitelist()
def get_medical_records_by_patient(patient_id):
    return frappe.get_all(
        "Medical Record",
        filters={"patient": patient_id},
        fields=["name", "record_type", "notes", "diagnosis", "test_results", "appointment", "creation"]
    )

@frappe.whitelist()
def get_prescriptions(record_id):
    record = frappe.get_doc("Medical Record", record_id)
    return record.prescriptions
