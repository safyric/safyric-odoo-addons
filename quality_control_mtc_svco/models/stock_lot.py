from odoo import api, fields, models

class StockLot(models.Model):
    _inherit = 'stock.lot'

    mtc_id = fields.Many2one('qc.mtc', string='MTC', ondelete='set null')
    sale_order_ids = fields.Many2many(store=True)
