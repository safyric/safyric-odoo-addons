from odoo import api, fields, models

class ProductPriceExtra(models.Model):
    _inherit = 'product.product'

    @api.depends('list_price', 'price_extra', 'product_template_attribute_value_ids.price_extra_pct')
    def _compute_product_lst_price(self):
        to_uom = None
        if 'uom' in self._context:
            to_uom = self.env['uom.uom'].browse([self._context['uom']])

        for product in self:
            if to_uom:
                list_price = product.uom_id._compute_price(product.list_price, to_uom)
            else:
                list_price = product.list_price
            price_extra_pct = sum(product.mapped('product_template_attribute_value_ids.price_extra_pct'))
            product.lst_price = list_price + list_price * price_extra_pct / 100 + product.price_extra

        return super(ProductProduct,self)._compute_product_lst_price(self)
