# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Shipping Invoice",
    'summary': "Add option to create commercial invoice for shipping as per delivery slip.",
    "author": "Safyric Co., Ltd.",
    "version": "12.0.1.0.0",
    "category": "Warehouse",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "depends": [
        "stock",
        "sale_stock",
        "stock_views_extension",
    ],
    "data": [
        "views/stock_report_layout.xml",
        "views/report_shipping_invoice.xml",
        "views/stock_picking_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
