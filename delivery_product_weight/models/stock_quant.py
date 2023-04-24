from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    product_weight = fields.Float('Product Weight', digits=dp.get_precision('Stock Weight'))

    def _update_product_weight(self):
        self = self.sudo()        
        for quant in self:
            if quant.product_id:
                quant.product_weight = quant.product_id.weight

class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'
    
    @api.one
    @api.depends('quant_ids', 'packaging_id')
    def _compute_weight(self):
        res = super(StockQuantPackage, self)._compute_weight()
        weight = 0.0
        package_weight = 0.0
        picking_state = self.env.context.get('default_picking_state')
        picking_id = self.env.context.get('picking_id')
        if picking_id:
            current_picking_move_line_ids = self.env['stock.move.line'].search([('result_package_id', '=', self.id), ('picking_id', '=', self.env.context['picking_id'])])
            for ml in current_picking_move_line_ids:
                weight += ml.product_uom_id._compute_quantity(ml.qty_done,ml.product_id.uom_id) * ml.product_weight
        else:
            for quant in self.quant_ids:
                weight += quant.quantity * quant.product_weight
                    
        if self.packaging_id and self.packaging_id.weight > 0 and picking_state != "done":
            package_weight = self.packaging_id.weight
        
        self.weight = weight
        self.shipping_weight = package_weight
        return res
    
