from odoo import api, field

class StockPicking(models.Model):

    _inherit = 'stock.picking'
    
    
    shipping_date = fields.Date(string='Shipping Date')
