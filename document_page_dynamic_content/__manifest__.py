{
    "name": "Document Page Dynamic Content",
    "version": "12.0.1.0.0",
    "author": "Safyric Valve Co., Ltd.",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "license": "AGPL-3",
    "category": "Generic Modules/Others",
    "depends": [
        'document_page',
        'mgmtsystem'
    ],
    "data": [
	'security/ir.model.access.csv',
        'views/document_page.xml',
	'views/document_page_content.xml',
        'views/report_document_page.xml',
    ],
    'installable': True,
}
