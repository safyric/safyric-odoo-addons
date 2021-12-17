# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Order Digitized Signature",
    "summary": "Capture customer signature on the purchase order",
    "version": "12.0.1.0.0",
    "author": "Safyric Co., Ltd.",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "category": "Purchase",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "web_widget_digitized_signature",
    ],
    "data": [
        "report/report_purchaseorder.xml",
        "views/purchase_views.xml",
    ],
    "installable": True,
}
