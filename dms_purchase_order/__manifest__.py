# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "DMS Purchase Order",
    "summary": """
        DMS files related to Purchase Order""",
    "version": "12.0.1.0.1",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "depends": [
	"dms",
        "purchase"
    ],
    "data": [
        "views/dms_file.xml",
	"views/purchase_order.xml",
	"views/report_purchase.xml"
    ],
}
