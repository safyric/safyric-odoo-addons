{
    'name': 'Quality Control ITP',
    'version': '2.0',
    'category': 'Quality control',
    'summary': 'Inspection and Test Plan for Quality Control',
    'website': 'https://www.github.com/safyric/safyric-odoo-addons',
    'depends': ['quality_control'],
    'data': [
        'security/quality_control_itp_security.xml',
        'security/ir.model.access.csv',
        'data/quality_control_itp_data.xml',
        'data/quality_control_itp_sequence.xml',
        'wizard/quality_control_itp_register.xml',
        'views/quality_control_itp_views.xml',
        'report/quality_control_itp_report.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
