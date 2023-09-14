# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Inventory Views Extension",
    'summary': "Extend views to customize as per company",
    "author": "Safyric Co., Ltd.",
    "version": "12.0.1.0.0",
    "category": "Warehouse",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "depends": [
        "stock",
        "sale_stock",
        "delivery",
        "purchase"
    ],
    "data": [
        "reports/stock_report_layout.xml",
        "reports/report_deliveryslip.xml",
        "reports/report_picking.xml",
	"reports/report_packinglist.xml",
        "views/stock_move_view.xml",
        "views/stock_picking_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
