# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Digitized Signature",
    "summary": "Capture customer signature on the invoices",
    "version": "12.0.1.0.0",
    "author": "Safyric Co., Ltd.",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "category": "Account",
    "license": "AGPL-3",
    "depends": [
        "account",
        "web_widget_digitized_signature",
    ],
    "data": [
        "views/report_invoice.xml",
        "views/account_invoice_view.xml",
    ],
    "installable": True,
}
