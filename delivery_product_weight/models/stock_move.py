from odoo import api, fields, models, _

from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_weight = fields.Float('Product Weight', digits=dp.get_precision('Stock Weight'))

    @api.depends('product_id', 'product_uom_qty', 'product_uom', 'product_weight')
    def _cal_move_weight(self):
        res = super(StockMove, self)._cal_move_weight()
        for move in self:
            move.weight = (move.product_qty * move.product_weight)
        return res

    def _action_assign(self):
        record = super(StockMove, self)._action_assign()
        for move in self:
            if move.product_weight <= 0.00 and move.product_id.weight !=0:
                move.product_weight = move.product_id.weight
            for line in move.move_line_ids:
                for quant in line.package_id.quant_ids:
                    quant.product_weight = move.product_weight

        return record

    @api.onchange('product_id')
    def onchange_product_id(self):
        res1 = super(StockMove, self).onchange_product_id()
        if self.product_id.weight > 0:
            self.product_weight = self.product_id.weight
        return res1


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_weight = fields.Float('Product Weight', digits=dp.get_precision('Stock Weight'), related='move_id.product_weight')

    @api.onchange('product_id', 'product_uom_id')
    def onchange_product_id(self):
        res = super(StockMoveLine, self).onchange_product_id()
        if self.product_id and self.result_package_id:
            for quant in self.result_package_id.quant_ids:
                quant.product_weight = self.product_weight
        return res
