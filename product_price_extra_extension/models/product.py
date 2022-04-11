from odoo import api, fields, models

class ProductPriceExtra(models.Model):
    _inherit = 'product.product'

    price_extra_pct = fields.Float(
        'Variant Price Extra %', compute='_compute_product_price_extra_pct',
        digits=dp.get_precision('Product Price'),
        help="This is the sum of the extra price in % of all attributes")
    
    @api.depends('product_template_attribute_value_ids.price_extra_pct')
    def _compute_product_price_extra_pct(self):
        for product in self:
            product.price_extra_pct = sum(product.mapped('product_template_attribute_value_ids.price_extra_pct'))

    @api.depends('list_price', 'price_extra', 'price_extra_pct')
    def _compute_product_lst_price(self):
        to_uom = None
        if 'uom' in self._context:
            to_uom = self.env['uom.uom'].browse([self._context['uom']])

        for product in self:
            if to_uom:
                list_price = product.uom_id._compute_price(product.list_price, to_uom)
            else:
                list_price = product.list_price
            product.lst_price = (list_price + product.price_extra) * (1 + product.price_extra_pct / 100)

        return super(ProductProductExtra,self)._compute_product_lst_price()
