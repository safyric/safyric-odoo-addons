# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Picking Fill Done Qty',
    'summary': 'Add button to fill and unfill done quantity',
    'version': '12.0.1.0.0',
    'category': 'Warehouse Management',
    'author': "Safyric valve Co., Ltd.",
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_move_view.xml',
    ],
    'installable': True,
    'license': "AGPL-3",
}
