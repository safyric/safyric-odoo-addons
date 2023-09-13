from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one('product.brand', 
        string='Brand')

    brand_ids = fields.Many2many('product.brand', 'sale_brand_rel', compute='compute_brand_ids')

    @api.depends('product_id')
    def compute_brand_ids(self):
        for rec in self:
            rec.brand_ids = False
            if rec.product_id:
                if rec.product_id.product_brand_ids:
                    rec.brand_ids = rec.product_id.product_brand_ids.ids
