// Copyright (c) 2019, vinhnguyen.t090@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Moka Settings', {
	refresh: function(frm) {
		frm.add_custom_button(__("Integration Request"), function() {
			frappe.route_options = {"integration_request_service": "Moka"};
			frappe.set_route("List", "Integration Request");
		});
		frm.add_custom_button(__("Payment Gateway Accounts"), function() {
			frappe.route_options = {"payment_gateway": "Moka"};
			frappe.set_route("List", "Payment Gateway Account");
		});
	}
});
