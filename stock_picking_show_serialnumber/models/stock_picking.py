from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    show_serial = fields.Boolean(string='Show Serial/Lot Number', default=False)
