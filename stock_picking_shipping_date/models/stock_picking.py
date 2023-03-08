from odoo import api, models, fields

class StockPicking(models.Model):

    _inherit = 'stock.picking'
    
    
    shipping_date = fields.Date(string='Shipping Date')
