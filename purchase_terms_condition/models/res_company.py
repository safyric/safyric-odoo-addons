from odoo import fields, models

class ResCompany(models.Model):

    _inherit = 'res.company'

    purchase_note = fields.Html(
        string='Purchase Default Terms and Conditions',
        translate=True)
