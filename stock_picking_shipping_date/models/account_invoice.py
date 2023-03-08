from odoo import api, models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    picking_id = fields.Many2one('stock.picking')
