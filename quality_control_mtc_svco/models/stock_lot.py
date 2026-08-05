from odoo import api, fields, models

class StockLot(models.Model):
    _inherit = 'stock.lot'

    mtc_id = fields.Many2one('qc.mtc', string='MTC', ondelete='set null')
    sale_order_ids = fields.Many2many('sale.order', string='Sale Orders', compute='_compute_sale_order_ids', store=False)
    sale_order_count = fields.Integer(compute='_compute_sale_order_ids', store=False)

    def _compute_sale_order_ids(self):
        for lot in self:
            # Implementation depends on how sales orders are linked to lots
            # This is a placeholder - adjust based on actual business logic
            lot.sale_order_ids = False
            lot.sale_order_count = 0
