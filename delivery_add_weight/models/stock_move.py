# -*- coding: utf-8 -*-

from odoo import api, fields, models

from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_weight = fields.Float(default='_calc_default_weight', digits=dp.get_precision('Stock Weight'), store=True, compute_sudo=True)
    
    @api.depends('product_id', 'product_uom_qty', 'product_uom')
    def _cal_move_weight(self):
        res = super(StockMove, self)._cal_move_weight()
        for move in self.filtered(lambda moves: moves.product_weight > 0.00):
            move.weight = (move.product_qty * move.product_weight)
        return res
        
    def _cal_default_weight(self):
        if self.product_id.weight:
            return self.product_id.weight
