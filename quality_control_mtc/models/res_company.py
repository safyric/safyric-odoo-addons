from odoo import fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    mtc_statement = fields.Text('Default Statement')
