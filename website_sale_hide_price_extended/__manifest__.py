# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Website Sale Hide Price Extended',
    'version': '12.0.1.0.0',
    'category': 'Website',
    'author': 'Safyric Co., Ltd.',
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'license': 'AGPL-3',
    'summary': 'Hide product prices on the shop',
    'depends': [
        'website_sale',
        'website_sale_hide_price',
    ],
    'data': [
        'views/website_sale_template.xml'
    ],
    'installable': True,
}
