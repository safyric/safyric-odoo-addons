# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Picking Digitized Signature",
    "summary": "Capture customer signature on the shipping documents",
    "version": "12.0.1.0.0",
    "author": "Safyric Co., Ltd.",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "category": "Purchase",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "web_widget_digitized_signature",
    ],
    "data": [
        "views/report_deliveryslip.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
