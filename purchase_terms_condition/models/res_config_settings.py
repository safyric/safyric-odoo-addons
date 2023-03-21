from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_notes = fields.Html(
        related='company_id.purchase_note',
        string="Purchase Terms & Conditions",
        default_model="purchase.order",
        readonly=False)
