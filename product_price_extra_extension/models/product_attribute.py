from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

class ProductTemplateAttributeValueInherit(models.Model):
    _inherit = "product.template.attribute.value"

    price_extra_pct = fields.Float(
        string='Attribute Price Extra %',
        default=0.0,
        digits=dp.get_precision('Product Price'))
