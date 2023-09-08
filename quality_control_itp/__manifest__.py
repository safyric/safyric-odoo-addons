{
    'name': 'Quality Control ITP',
    'version': '2.0',
    'category': 'Quality control',
    'summary': 'Inspection and Test Plan for Quality Control',
    'website': 'https://www.github.com/safyric/safyric-odoo-addons',
    'depends': [
	'quality_control',
	'sale',
	'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/quality_control_itp_views.xml',
        'report/quality_control_itp_report.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
