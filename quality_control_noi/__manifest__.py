{
    "name": "Quality Control NOI",
    "summary": "Allow to manage notification of inspections.",
    "version": "12.0.1.0.1",
    "development_status": "Production/Stable",
    "category": "Quality Control",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "author": "Safyric Co., Ltd.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "quality_control",
        "sale",
	"purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/quality_control_noi_security.xml",
        "data/qc_noi_sequence.xml",
        "views/qc_noi_view.xml",
	"views/qc_noi_report.xml",
    ],
}
