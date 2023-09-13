from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one('product.brand', 
        string='Brand')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.brand_id = False
            brands = self.product_id.product_brand_ids.ids
            if brands:
                domain = [('id', 'in', brands)]
                return {'domain': {'brand_id': domain}}
        return {'domain': {'brand_id': [('id', 'in', [])]}}
