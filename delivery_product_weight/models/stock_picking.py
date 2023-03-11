from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    @api.one
    @api.depends('move_line_ids', 'move_line_ids.result_package_id', 'move_line_ids.product_uom_id', 'move_line_ids.qty_done')
    def _compute_bulk_weight(self):
        weight = 0.0
        for move_line in self.move_line_ids:
            if move_line.product_id and move_line.product_weight > 0:
                weight += move_line.product_uom_id._compute_quantity(move_line.qty_done, move_line.product_id.uom_id) * move_line.product_weight
            else:
                weight += move_line.product_uom_id._compute_quantity(move_line.qty_done, move_line.product_id.uom_id) * move_line.product_id.weight
        self.weight_bulk = weight
        return super(StockPicking, self)._compute_bulk_weight()

    @api.multi
    def write(self, vals):
        res = super(Picking, self).write(vals)
        for move_line in self.move_line_ids:
            if move_line.product_id and move_line.product_weight > 0:
                move_line.product_id.weight = move_line.product_weight
        return res
