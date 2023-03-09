from odoo import api, models, fields

class StockPicking(models.Model):

    _inherit = 'stock.picking'
    
    
    shipping_date = fields.Date(string='Shipping Date')

    def get_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree',
            'res_model': 'account.invoice',
            'domain': [('picking_id', '=', self.id)],
            'context': "{'create': False}"
        }
    
    invoice_count = fields.Integer(compute='compute_count')
    
    def compute_count(self):
    for record in self:
        record.invoice_count = self.env['account.invoice'].search_count(
            [('picking_id', '=', self.id)])
