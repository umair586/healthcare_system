import frappe
from .jwt_auth import authenticate

@frappe.whitelist()
@authenticate()
def kpis(doctor_id):

    today = frappe.utils.today()
    week_ago = frappe.utils.add_days(today, -7)

    return {
        "total_today": frappe.db.count("Appointment", {
            "doctor": doctor_id, "date": today
        }),
        "completed_today": frappe.db.count("Appointment", {
            "doctor": doctor_id, "date": today, "status": "Completed"
        }),
        "pending_today": frappe.db.count("Appointment", {
            "doctor": doctor_id, "date": today, "status": "Pending"
        }),
        "unique_patients_week": frappe.db.sql("""
            SELECT COUNT(DISTINCT patient)
            FROM `tabAppointment`
            WHERE doctor = %s AND date >= %s
        """, (doctor_id, week_ago))[0][0]
    }
    
    
@frappe.whitelist()
@authenticate()
def calendar_events(doctor_id):

    today = frappe.utils.today()
    end = frappe.utils.add_days(today, 30)

    appointments = frappe.get_all("Appointment",
        filters={"doctor": doctor_id, "date": ["between", [today, end]]},
        fields=["name", "date", "time", "patient", "status"]
    )

    events = []
    for appt in appointments:
        events.append({
            "title": f"{appt.patient} ({appt.status})",
            "start": f"{appt.date}T{appt.time}",
            "end": f"{appt.date}T{appt.time}",
            "status": appt.status
        })

    return events


@frappe.whitelist()
@authenticate()
def appointment_trend(doctor_id):

    records = frappe.db.sql("""
        SELECT date, COUNT(*) as count
        FROM `tabAppointment`
        WHERE doctor = %s AND date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)
        GROUP BY date ORDER BY date ASC
    """, (doctor_id,), as_dict=True)

    return records


@frappe.whitelist()
@authenticate()
def status_distribution(doctor_id):

    result = frappe.db.sql("""
        SELECT status, COUNT(*) as total
        FROM `tabAppointment`
        WHERE doctor = %s
        GROUP BY status
    """, (doctor_id,), as_dict=True)

    return result
