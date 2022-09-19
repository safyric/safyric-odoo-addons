from odoo import fields, models


class HrEmpolyee(models.Model):
    _inherit = 'hr.employee'

    name = fields.Char(translate=True)
    work_location = fields.Char(translate=True)
