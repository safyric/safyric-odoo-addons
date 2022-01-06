from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


    
class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    product_weight = fields.Float('Product Weight', digits=dp.get_precision('Stock Weight'))    
    

class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    @api.one
    @api.depends('quant_ids')
    def _compute_weight(self):
        weight = 0.0
        if self.env.context.get('picking_id'):
            current_picking_move_line_ids = self.env['stock.move.line'].search([('result_package_id', '=', self.id), ('picking_id', '=', self.env.context['picking_id'])])
            for ml in current_picking_move_line_ids:
                if ml.product_weight > 0:
                    weight += ml.product_uom_id._compute_quantity(ml.qty_done,ml.product_id.uom_id) * ml.product_weight
                else:
                    weight += ml.product_uom_id._compute_quantity(ml.qty_done,ml.product_id.uom_id) * ml.product_id.weight
        else:
            for quant in self.quant_ids:
                if quant.product_weight > 0:
                    weight += quant.quantity * quant.product_weight
                else:
                    weight += quant.quantity * quant.product_id.weight
        self.weight = weight
        
