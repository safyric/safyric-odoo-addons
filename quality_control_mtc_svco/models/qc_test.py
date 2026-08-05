from odoo import api, fields, models

class QcTest(models.Model):
    _inherit = 'qc.test'

    type = fields.Selection(
        selection_add=[('material', 'Material')],
        ondelete={'material': 'cascade'}
    )

