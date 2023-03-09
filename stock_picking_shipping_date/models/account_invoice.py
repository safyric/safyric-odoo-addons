from odoo import api, models, fields, _

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    picking_id = fields.Many2one('stock.picking')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for rec in self:
            return {'domain': {'picking_id': ['|', ('partner_id', '=', rec.partner_id.id), ('partner_id', '=', rec.partner_shipping_id.id)]}}
        return super(AccountInvoice, self)._onchange_partner_id()
    
