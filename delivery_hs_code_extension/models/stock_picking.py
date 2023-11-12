from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_preferential_duty = fields.Boolean('Preferential Duty', default=False)
