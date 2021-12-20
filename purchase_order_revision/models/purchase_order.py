from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
   
    current_revision_id = fields.Many2one('purchase.order','Current revision',readonly=True,copy=True)
    old_revision_ids = fields.One2many('purchase.order','current_revision_id','Old revisions',readonly=True)
    revision_number = fields.Integer('Revision',copy=False)
    unrevisioned_name = fields.Char('Order Reference',copy=False,readonly=True)
    active = fields.Boolean('Active',default=True,copy=True)    
    
    @api.model
    def create(self, vals):
        if 'unrevisioned_name' not in vals:
            if vals.get('name', 'New') == 'New':
                seq = self.env['ir.sequence']
                vals['name'] = seq.next_by_code('purchase.order') or '/'
            vals['unrevisioned_name'] = vals['name']
        return super(PurchaseOrder, self).create(vals)
    
