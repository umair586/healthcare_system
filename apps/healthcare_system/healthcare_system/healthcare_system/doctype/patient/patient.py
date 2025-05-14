# Copyright (c) 2025, Umair Tariq and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Patient(Document):
	def validate(self):
		if self.age <= 0:
			frappe.throw("Age must be greater than 0")
		if not self.email or not frappe.utils.validate_email_address(self.email):
			frappe.throw("Invalid email address")