from odoo import api, fields, models

class StockProductionLot(models.Model):
    _inherit='stock.production.lot'

    mtc_id = fields.Many2one('qc.mtc', string='MTC')
    sale_order_ids = fields.Many2many(store=True)
