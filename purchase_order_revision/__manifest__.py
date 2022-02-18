# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Purchase Order Revision",
    'summary': 'Keep track of revised quotations',
    "author": "Safyric Co., Ltd.",
    "version": "12.0.1.0.0",
    "category": "Purchase Management",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "depends": [
        "purchase",
        "purchase_stock",
    ],
    "data": [
        "views/purchase_order.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
    "post_init_hook": "populate_unrevisioned_name",
}
