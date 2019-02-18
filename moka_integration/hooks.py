# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "moka_integration"
app_title = "Moka Integration"
app_publisher = "vinhnguyen.t090@gmail.com"
app_description = "Moka Payment Gateway Integration"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "vinhnguyen.t090@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/moka_integration/css/moka_integration.css"
# app_include_js = "/assets/moka_integration/js/moka_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/moka_integration/css/moka_integration.css"
# web_include_js = "/assets/moka_integration/js/moka_integration.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "moka_integration.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "moka_integration.install.before_install"
# after_install = "moka_integration.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "moka_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# vinh
# doc_events = {
# 	"Payment Request": {
# 		"validate": "moka_integration.moka_integration.doctype.moka_settings.moka_settings.validate_moka_credentials",
# 		"get_payment_url": "moka_integration.utils.get_payment_url"
# 	},
# 	"Shopping Cart Settings": {
# 		"validate": "moka_integration.utils.validate_price_list_currency"
# 	}
# }


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"moka_integration.tasks.all"
# 	],
# 	"daily": [
# 		"moka_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"moka_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"moka_integration.tasks.weekly"
# 	]
# 	"monthly": [
# 		"moka_integration.tasks.monthly"
# 	]
# }


scheduler_events = {
	"all": [
		# vinh
		# "moka_integration.moka_integration.doctype.moka_payment.moka_payment.authorise_payment",
		# "moka_integration.moka_integration.doctype.moka_settings.moka_settings.capture_payment"
	]
}

# Testing
# -------

# before_tests = "moka_integration.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "moka_integration.event.get_events"
# }

