from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    @api.one
    @api.depends('move_line_ids', 'move_line_ids.result_package_id', 'move_line_ids.product_uom_id', 'move_line_ids.qty_done')
    def _compute_bulk_weight(self):
        res = super(StockPicking, self)._compute_bulk_weight()
        weight = 0.0
        for move_line in self.move_line_ids:
            if move_line.product_id:
                weight += move_line.product_uom_id._compute_quantity(move_line.qty_done, move_line.product_id.uom_id) * move_line.product_weight

        self.weight_bulk = weight
        return res

    @api.multi
    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        for picking in self:
            for ml in picking.move_line_ids:
                if ml.product_id and ml.product_weight != ml.product_id.weight:
                    ml.product_id.weight = ml.product_weight
                for quant in ml.result_package_id.quant_ids:
                    if self.state != 'done':
                        quant._update_product_weight()
        return res

    @api.multi
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for picking in self:
            for move in picking.move_lines:
                move._update_shipping_weight()
        return res

    @api.multi
    def button_update_weight(self):
        for picking in self:
            for move in picking.move_lines:
                move._update_shipping_weight()
