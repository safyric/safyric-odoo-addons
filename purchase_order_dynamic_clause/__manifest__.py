{
    'name': 'Purchase Order Dynamic Clauses',
    'version': '12.0.1.1',
    'summary': 'Purchase Order Dynamic Clauses',
    'description': 'Allow to dynamically generate the clauses for Purchase Order',
    'depends': [
	'purchase',
    ],
    'data': [
	'security/ir.model.access.csv',
	'views/purchase_order.xml',
	'views/purchase_clause.xml',
	'views/report_purchase_order.xml'
    ],
    'author': 'Safyric Valve Co., Ltd.',
    'website': 'https://github.com/safyric-odoo-addons',
    'license': 'AGPL-3',
    'installable': True,
}
