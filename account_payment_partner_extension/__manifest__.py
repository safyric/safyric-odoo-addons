# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Payment Partner Extended',
    'version': '12.0.1.0.0',
    'category': 'Banking addons',
    'license': 'AGPL-3',
    'summary': 'Adds payment mode on partners and invoices',
    'author': "Safyric Co., Ltd.",
    'website': 'https://github.com/OCA/bank-payment',
    'depends': [
        'account_payment_partner',
        'account',
    ],
    'data': [
        'views/report_invoice.xml',
    ],
    'installable': True,
}
