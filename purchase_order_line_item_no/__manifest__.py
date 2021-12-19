# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

{
    "name": "Purchase Order Line Item No",
    "version": "12.0.0.1",
    "summary": "Adds item number to each sale order line.",
    "author": "Safyric Co., Ltd.",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "category": "Sale",
    "license": "AGPL-3",
    "depends": [
        "purchase",
    ],
    "data": [
        "views/purchase_order_view.xml",
        "views/portal_template.xml",
    ],
    "installable": True,
}
