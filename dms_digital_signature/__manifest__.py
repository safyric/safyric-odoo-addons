# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "DMS Digital Signature",
    "summary": """
        Digitally sign documents""",
    "version": "12.0.1.0.1",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "depends": [
	"dms",
	"report_qweb_signer",
        "base_users_signatures"
    ],
    "data": [
        "wizards/dms_digital_signature.xml",
        "views/dms_file.xml",
    ],
}
