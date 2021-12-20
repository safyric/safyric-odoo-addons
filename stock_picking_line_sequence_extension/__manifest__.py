# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock picking lines sequence extension',
    'summary': 'Manages the order of stock moves by displaying its sequence',
    'version': '12.0.1.0.0',
    'category': 'Warehouse Management',
    'author': "Safyric Co., Ld.",
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'depends': ['stock_picking_line_sequence'],
    'data': [
        'views/report_deliveryslip.xml',
    ],
    'installable': True,
    'license': "AGPL-3",
}
