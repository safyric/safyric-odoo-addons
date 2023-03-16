from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

    

class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"
    
    shipping_weight = fields.Float(string='Shipping Weight', compute='_compute_weight', help="Weight used to compute the price of the delivery (if applicable).")

    @api.one
    @api.depends('quant_ids', 'packaging_id')
    def _compute_weight(self):
        res = super(StockQuantPackage, self)._compute_weight()
        weight = 0.0
        if self.env.context.get('picking_id'):
            current_picking_move_line_ids = self.env['stock.move.line'].search([('result_package_id', '=', self.id), ('picking_id', '=', self.env.context['picking_id'])])
            for ml in current_picking_move_line_ids:
                if ml.product_weight > 0:
                    weight += ml.product_uom_id._compute_quantity(ml.qty_done,ml.product_id.uom_id) * ml.product_weight
                else:
                    weight += ml.product_uom_id._compute_quantity(ml.qty_done,ml.product_id.uom_id) * ml.product_id.weight
        
        self.weight = weight
        self.shipping_weight = weight + self.packaging_id.weight
        return res
