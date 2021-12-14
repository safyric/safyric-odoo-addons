# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Portal View Extension',
    'version': '12.0.1.0.0',
    'category': 'Website',
    'author': 'Safyric Co., Ltd.',
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'license': 'AGPL-3',
    'summary': 'Extend portal views and modify according to company requirements',
    'depends': [
        'portal',
        'sale',
        'account',
    ],
    'data': [
        'views/sale_portal_template.xml',
        'views/account_portal_template.xml',
    ],
    'installable': True,
}
