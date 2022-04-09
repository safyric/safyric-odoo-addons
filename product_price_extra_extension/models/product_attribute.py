from odoo import api, fields

class ProductTemplateAttributeValueInherit(models.Model):
    _inherit = "product.template.attribute.value"

    price_extra_pct = fields.Boolean('is pct?')
