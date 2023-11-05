import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)

class SaleOrderDigitalSignature(models.TransientModel):
    _name = "sale.order.digital.signature"
    _description = "Sale order Digital Signature"

    signature_id = fields.Many2one('res.users.signatures', string='Signature')
    signature = fields.Binary(string='Signature', attachment=False)
    signature_keyword = fields.Char('Signature Area', help="Keyword to identify the signature area to attach digital signature")
    signature_width = fields.Integer('Signature Width', help="Width of the signature area")
    signature_height = fields.Integer('Signature Height', help="Height of the signature area")


    @api.onchange('signature_id')
    def _onchange_signature_id(self):
        if self.signature_id:
            self.signature = self.signature_id.digital_signature
        else:
            self.signature = False


    @api.multi
    def sale_order_digital_signature(self):
        docs = self.env['sale.order'].browse(self._context.get('active_ids', []))

        data = {}
        data.update({
            'sig_img': self.signature,
            'keyword': self.signature_keyword,
            'width': self.signature_width,
            'height': self.signature_height,
            'res_ids': docs.ids
        })

        return self.env.ref('sale.action_report_saleorder').report_action(self, data=data)
