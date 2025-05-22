import frappe
from frappe.utils import nowdate, add_days

def send_daily_appointment_reminders():
    tomorrow = add_days(nowdate(), 1)

    appointments = frappe.get_all("Appointment",
        filters={
            "date": tomorrow,
            "status": ["in", ["Pending", "Confirmed"]],
        },
        fields=["name", "patient", "doctor", "date", "time"]
    )

    for appt in appointments:
        # Fetch patient email from linked Patient DocType
        patient_doc = frappe.get_doc("Patient", appt.patient)
        patient_email = patient_doc.email if hasattr(patient_doc, "email") else None

        if not patient_email:
            frappe.logger().info(f"No email found for Patient {appt.patient}")
            continue

        # Send Email
        frappe.sendmail(
            recipients=[patient_email],
            subject=f"Appointment Reminder for {appt.patient}",
            message=f"""
                Dear {patient_doc.full_name},<br><br>
                This is a reminder for your appointment:<br>
                Doctor: {appt.doctor}<br>
                Date: {appt.date}<br>
                Time: {appt.time}<br><br>
                Thank you,<br>Clinic Team
            """
        )
