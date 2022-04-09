from odoo import api, fields, models

class ProductTemplateAttributeValueInherit(models.Model):
    _inherit = "product.template.attribute.value"

    price_extra_pct = fields.Boolean('Is price percentage?')
