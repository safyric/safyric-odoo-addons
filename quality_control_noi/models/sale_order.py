from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    noi_id = fields.Many2one('qc.noi', string='NOI')
