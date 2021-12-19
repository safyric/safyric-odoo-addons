# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Sale Views Extension',
    'version': '12.0.1.0.1',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Extend views to customize as per company',
    'depends': [
        'sale',
    ],
    'author': 'Safyric Co., Ltd.',
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'data': [
        'views/sale_report_layout.xml',
        'views/sale_order_views.xml',
        'views/sale_report_template.xml',
    ],
    'installable': True,
}
