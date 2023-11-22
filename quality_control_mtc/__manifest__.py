{
    'name': 'Quality Control MTC',
    'version': '2.0',
    'category': 'Quality control',
    'summary': 'Mill Test Certificate',
    'website': 'https://www.github.com/safyric/safyric-odoo-addons',
    'depends': [
	'quality_control',
	'sale',
	'sale_stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/quality_control_mtc_views.xml',
	'report/qc_mtc_report.xml',
        'report/qc_mtc_report_layout.xml',
	'report/qc_mtc_report_template.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
