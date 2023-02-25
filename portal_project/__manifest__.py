# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Portal Project',
    'version': '12.0.1.0.0',
    'category': 'Website',
    'author': 'Safyric Co., Ltd.',
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'license': 'AGPL-3',
    'summary': 'Extend portal for projects and tasks',
    'depends': [
        'portal',
        'project',
    ],
    'data': [
        'views/project_portal_template.xml',
    ],
    'installable': True,
}
