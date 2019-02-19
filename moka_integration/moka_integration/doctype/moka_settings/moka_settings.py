# -*- coding: utf-8 -*-
# Copyright (c) 2019, vinhnguyen.t090@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json
from six.moves.urllib.parse import urlencode
from frappe.model.document import Document
from frappe.utils import get_url, call_hook_method, cint
from frappe.integrations.utils import make_get_request, make_post_request, create_request_log, create_payment_gateway
from six.moves.urllib.parse import urlparse, parse_qs

class MokaSettings(Document):
	supported_currencies = ["TRY","USD", "EUR", "GBP"]

	def validate(self):
		create_payment_gateway('Moka')
		call_hook_method('payment_gateway_enabled', gateway='Moka')

	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			frappe.throw(_("Please select another payment method. Moka does not support transactions in currency '{0}'").format(currency))

	def get_payment_url(self, **kwargs):
		integration_request = create_request_log(kwargs, "Host", "Moka")
		return get_url("/moka_checkout?token={0}".format(integration_request.name))


@frappe.whitelist(allow_guest=True)
def confirm_payment(**kwargs):
	try:
		redirect = True
		status_changed_to, redirect_to = None, None

		query = dict(parse_qs(urlparse(frappe.local.request.url).query))
		token = query['token'][0]

		integration_request = frappe.get_doc("Integration Request", token)
		data = json.loads(integration_request.data)

		redirect_to = data.get('redirect_to') or None
		redirect_message = data.get('redirect_message') or None

		if kwargs.get("isSuccessful") == "True":
			if data.get("reference_doctype") and data.get("reference_docname"):
				custom_redirect_to = frappe.get_doc(data.get("reference_doctype"),
					data.get("reference_docname")).run_method("on_payment_authorized", "Completed")
				frappe.db.commit()

				if custom_redirect_to:
					custom_redirect_to = "/"+custom_redirect_to
					redirect_to = custom_redirect_to

			redirect_url = '/integrations/payment-success'
		else:
			redirect_url = "/integrations/payment-failed"

		if redirect_to:
			redirect_url += '?' + urlencode({'redirect_to': redirect_to})
		if redirect_message:
			redirect_url += '&' + urlencode({'redirect_message': redirect_message})

		# this is done so that functions called via hooks can update flags.redirect_to
		if redirect:
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = get_url(redirect_url)

	except Exception:
		frappe.log_error(frappe.get_traceback())


def update_integration_request_status(token, data, status, error=False):
	frappe.get_doc("Integration Request", token).update_status(data, status)		
