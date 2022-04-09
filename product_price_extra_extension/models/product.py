from odoo import api, fields, models

class ProductPriceExtra(models.Model):
    _inherit = 'product.product'

    @api.depends('product_template_attribute_value_ids.price_extra', 'product_template_attribute_value_ids.price_extra_pct')
    def _compute_product_price_extra(self):
        for product in self:
            product.price_extra = sum(product.mapped('product_template_attribute_value_ids.price_extra')) \
            + sum(product.mapped('product_template_attribute_value_ids.price_extra_pct')) * product.price
