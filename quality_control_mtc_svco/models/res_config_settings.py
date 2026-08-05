from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mtc_statement = fields.Text(related='company_id.mtc_statement', string="Default Statement", readonly=False)

