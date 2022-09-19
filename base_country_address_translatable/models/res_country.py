from odoo import fields, models


class CountryState(models.Model):
    _inherit = 'res.country'

    address_format = fields.Text(translate=True)
