import frappe
from .jwt_auth import authenticate

@frappe.whitelist()
@authenticate(["System Manager", "Hospital Admin"])
def get_admin_dashboard():

    return {
        "total_patients": frappe.db.count("Patient"),
        "total_doctors": frappe.db.count("Doctor"),
        "total_appointments": frappe.db.count("Appointment"),
        "completed_appointments": frappe.db.count("Appointment", {"status": "Completed"}),
        "pending_appointments": frappe.db.count("Appointment", {"status": "Pending"}),
    }


@frappe.whitelist()
@authenticate(["System Manager"])
def get_users_with_roles():

    users = frappe.get_all("User", filters={"enabled": 1}, fields=["name", "full_name", "email"])
    for u in users:
        u["roles"] = [r.role for r in frappe.get_all("Has Role", filters={"parent": u["name"]}, fields=["role"])]
    return users


@frappe.whitelist()
@authenticate(["Hospital Admin"])
def get_appointment_report(status=None, doctor=None):

    filters = {}
    if status: filters["status"] = status
    if doctor: filters["doctor"] = doctor

    return frappe.get_all("Appointment", filters=filters,
        fields=["name", "patient", "doctor", "status", "date", "time"],
        order_by="date desc", limit_page_length=50)


@frappe.whitelist()
@authenticate(["Hospital Admin"])
def doctor_performance_api():

    result = frappe.db.sql("""
        SELECT 
            doctor,
            COUNT(name) AS total_appointments,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed
        FROM
            `tabAppointment`
        GROUP BY doctor
    """, as_dict=True)
    return result
