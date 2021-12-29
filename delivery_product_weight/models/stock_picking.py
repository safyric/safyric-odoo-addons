from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    @api.one
    @api.depends('move_line_ids', 'move_line_ids.result_package_id', 'move_line_ids.product_uom_id', 'move_line_ids.qty_done')
    def _compute_bulk_weight(self):
        weight = 0.0
        for move_line in self.move_line_ids:
            if move_line.product_id:
                weight += move_line.product_uom_id._compute_quantity(move_line.qty_done, move_line.product_id.uom_id) * move_line.product_weight
        self.weight_bulk = weight


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    @api.one
    @api.depends('quant_ids')
    def _compute_weight(self):
        weight = 0.0
        if self.env.context.get('picking_id'):
            current_picking_move_line_ids = self.env['stock.move.line'].search([('result_package_id', '=', self.id), ('picking_id', '=', self.env.context['picking_id'])])
            for ml in current_picking_move_line_ids:
                weight += ml.product_uom_id._compute_quantity(ml.qty_done,ml.product_id.uom_id) * ml.product_weight
        else:
            for quant in self.quant_ids:
                weight += quant.quantity * quant.product_id.weight
        self.weight = weight
