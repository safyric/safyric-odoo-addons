from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_weight = fields.Float('Product Weight', digits=dp.get_precision('Stock Weight'))

    @api.depends('product_id', 'product_uom_qty', 'product_uom')
    def _cal_move_weight(self):
        for move in self:
            if move.product_weight > 0:
                move.weight = (move.product_qty * move.product_id.weight)
            else:
                move.weight = (move.product_qty * move.product_id.weight)

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

