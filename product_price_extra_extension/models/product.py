from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

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

    @api.multi
    def price_compute(self, price_type, uom=False, currency=False, company=False):
        # TDE FIXME: delegate to template or not ? fields are reencoded here ...
        # compatibility about context keys used a bit everywhere in the code
        if not uom and self._context.get('uom'):
            uom = self.env['uom.uom'].browse(self._context['uom'])
        if not currency and self._context.get('currency'):
            currency = self.env['res.currency'].browse(self._context['currency'])

        products = self
        if price_type == 'standard_price':
            # standard_price field can only be seen by users in base.group_user
            # Thus, in order to compute the sale price from the cost for users not in this group
            # We fetch the standard price as the superuser
            products = self.with_context(force_company=company and company.id or self._context.get('force_company', self.env.user.company_id.id)).sudo()

        prices = dict.fromkeys(self.ids, 0.0)
        for product in products:
            prices[product.id] = product[price_type] or 0.0
            if price_type == 'list_price':
                for line in product.product_tmpl_id.attribute_line_ids:
                    for value in product.attribute_value_ids.filtered(lambda r: r.attribute_id == line.attribute_id):
                        for price in value.price_ids.filtered(lambda r: r.product_tmpl_id == product.product_tmpl_id):
                            prices[product.id] = (prices[product.id] + price.price_extra) * (1 + price.price_extra_pct / 100)

            if uom:
                prices[product.id] = product.uom_id._compute_price(prices[product.id], uom)

            # Convert from current user company currency to asked one
            # This is right cause a field cannot be in more than one currency
            if currency:
                prices[product.id] = product.currency_id._convert(
                    prices[product.id], currency, product.company_id, fields.Date.today())

        return prices
