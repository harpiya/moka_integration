# @Author: Saadettin Yasir AKEL <developer>
# @Date:   2019-02-18T22:12:21+03:00
# @Email:  yasir@harpiya.com
# @Project: Harpiya Kurumsal Yönetim Sistemi
# @Filename: moka_checkout.py
# @Last modified by:   developer
# @Last modified time: 2019-02-18T22:42:01+03:00
# @License: MIT License. See license.txt
# @Copyright: Harpiya Yazılım Teknolojileri



# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, get_url
import json, hashlib, time
from six import string_types
from frappe.integrations.utils import make_get_request, make_post_request
import requests

no_cache = 1
no_sitemap = 1

expected_keys = ('amount', 'title', 'description', 'reference_doctype', 'reference_docname',
	'payer_name', 'payer_email', 'order_id', 'currency')

def get_context(context):
	context.no_cache = 1

	try:
		doc = frappe.get_doc("Integration Request", frappe.form_dict['token'])
		payment_details = json.loads(doc.data)

		for key in expected_keys:
			context[key] = payment_details[key]

		context['token'] = frappe.form_dict['token']
		context['amount'] = "{:.2f}".format(flt(context['amount']))

		moka = frappe.get_doc("Moka Settings")
		context['moka_sandbox'] = moka.moka_sandbox

	except Exception:
		frappe.redirect_to_message(_('Invalid Token'),
			_('Seems token you are using is invalid!'),
			http_status_code=400, indicator_color='red')

		frappe.local.flags.redirect_location = frappe.local.response.location
		raise frappe.Redirect

def replaceSpace(veri):
	veri =veri.replace("/s+/", "")
	veri =veri.replace(" ", "")
	veri =veri.replace("/s/g", "")
	veri =veri.replace("/s+/g", "")
	veri = veri.strip()
	return veri

@frappe.whitelist(allow_guest=True)
def make_checkout(data):

	data = json.loads(data)

	#get Moka Setting
	moka = frappe.get_doc("Moka Settings")

	dealercode = moka.moka_dealercode
	username = moka.moka_username
	password = moka.get_password(fieldname="moka_password", raise_exception=False)

	if moka.moka_sandbox == 1:
		moka_url = "https://service.testmoka.com"
	else:
		moka_url = "https://service.moka.com"


	if moka.moka_tdmode == 1:
		moka_url = moka_url + "/PaymentDealer/DoDirectPaymentThreeD"
	else:
		moka_url = moka_url + "/PaymentDealer/DoDirectPayment"


	#Convert Curreny ERPNext to MOKA
	if data["currency"] == 'TRY':
		currency = "TL"
	else:
		currency = data['currency']

	token = data['token']
	name = data['name']
	cvc = data['cvc']
	amount = data['amount']
	number = replaceSpace(data['number'])

	expiry = data['expiry']
	expiry = expiry.split('/')
	expiryMM = replaceSpace(expiry[0])
	expiryYY = replaceSpace(expiry[1])


	InstallmentNumber = 0
	OtherTrxCode = data['OtherTrxCode'] + "-" + str(cint(time.time()))
	SubMerchantName = ""
	RedirectUrl = get_url( \
			"/api/method/moka_integration.moka_integration.doctype.moka_settings.moka_settings.confirm_payment?token={0}".format(token))
	checkkey = hashlib.sha256(dealercode.encode('utf-8')+"MK"+username.encode('utf-8')+"PD"+password.encode('utf-8')).hexdigest()
	ClientIP = frappe.local.request_ip or '127.0.0.1'

	veri={
		"PaymentDealerAuthentication":{
			"DealerCode": dealercode,
			"Username": username,
			"Password": password,
			"CheckKey": checkkey
		},
		"PaymentDealerRequest":{
			'CardHolderFullName':name,
			'CardNumber':number,
			'ExpMonth':expiryMM,
			'ExpYear':'20'+expiryYY,
			'CvcNumber':cvc,
			'Amount':amount,
			'Currency': currency,
			'InstallmentNumber':InstallmentNumber,
			'ClientIP': ClientIP,
			'RedirectUrl':RedirectUrl,
			"RedirectType": 0,
			'OtherTrxCode':OtherTrxCode,
			'SubMerchantName':SubMerchantName
		}
	}

	headers = {
		"Content-Type": "application/json"
	}

	try:
		response = make_post_request(moka_url, headers=headers, data=json.dumps(veri))
		return response

	except Exception:
	 	frappe.log_error()
