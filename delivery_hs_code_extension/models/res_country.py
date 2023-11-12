from odoo import api, fields, models

class ResCountryGroup(models.Model):
    _inherit = 'res.country.group'

    type = fields.Selection([('normal', 'Normal'), ('eco', 'ECO'), ('trade', 'Trade Agreement')], default='normal', string="Group Type")
