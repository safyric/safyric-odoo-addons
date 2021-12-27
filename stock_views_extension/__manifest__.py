# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Inventory Views Extension",
    'summary': 'Extend views to customize as per company',
    "author": "Safyric Co., Ltd.",
    "version": "12.0.1.0.0",
    "category": "Warehouse",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "depends": [
        "stock",
        "sale_stock"
    ],
    "data": [
        "views/stock_report_layout.xml",
        "views/report_deliveryslip.xml",
        "views/report_picking.xml",
        "views/stock_picking_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
