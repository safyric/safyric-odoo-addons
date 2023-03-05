# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Invoicing Views Extension',
    'version': '12.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Extend views and reports for account module',
    'depends': [
        'account',
    ],
    'author': 'Safyric Co., Ltd.',
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'data': [
        'views/account_report_layout.xml',
        'views/account_invoice_report.xml',
        'views/invoice_report.xml',
    ],
    'installable': True,
}
