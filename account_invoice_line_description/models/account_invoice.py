from odoo import api, fields, models, _

class AccountInvoice(models.Model):

    _inherit = 'account.invoice'
    
    @api.multi
    def recalculate_names(self):
        for line in self.mapped('invoice_line_ids').filtered('product_id'):
            # we make this to isolate changed values:
            line2 = self.env['account.invoice.line'].new({
                'product_id': line.product_id,
            })
            line2._onchange_product_id()
            line.name = line2.name
        return True
