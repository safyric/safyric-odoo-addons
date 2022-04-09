from odoo import api, fields, models

class ProductPriceExtra(models.Model):
    _inherit = 'product.product'

    def _compute_product_price_extra(self):
        for product in self:
            price_extra = 0.0
            for attribute_id in product.mapped('product_template_attribute_value_ids'):
                if attribute_id.price_extra_pct:
                    price_extra = product.standard_price * attribute_id.price_extra / 100
                else:
                    price_extra = attribute_id.price_extra

            product.price_extra = price_extra
