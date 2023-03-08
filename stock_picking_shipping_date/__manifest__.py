# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Picking Shipping Date',
    'summary': 'Add shipping date to stock picking',
    'version': '12.0.1.0.0',
    'category': 'Warehouse Management',
    'author': "Safyric Co., Ltd.",
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'depends': [
        'stock',
        'account'
    ],
    'data': [
        'views/report_deliveryslip.xml',
        'views/stock_view.xml',
        'views/account_invoice_view.xml'
    ],
    'installable': True,
    'license': "AGPL-3",
}
