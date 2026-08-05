from odoo import api, fields, models

class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    show_on_mtc = fields.Boolean('Show On MTC', default=False)
