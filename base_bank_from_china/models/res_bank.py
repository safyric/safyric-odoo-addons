from odoo import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    cnaps_code = fields.Char()
