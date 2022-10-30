from odoo import fields, models


class ResPartnerBank(models.Model):

    _inherit = 'res.partner.bank'

    active = fields.Boolean(default=True)
    intermediary_bank_id = fields.Many2one('res.bank', string='Intermediary Bank')
