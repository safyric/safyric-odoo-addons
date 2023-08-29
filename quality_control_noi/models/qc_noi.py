# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Aleph Objects, Inc. (https://www.alephobjects.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class QcNoi(models.Model):
    _name = 'qc.noi'
    _description = 'Inspection Notification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'qc.noi') or ''
        return super(QcNoi, self).create(vals)

    name = fields.Char(readonly=True)
    date = fields.Datetime(string='Date', required=True, copy=False, default=fields.Datetime.now)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    responsible_id = fields.Many2one('res.users', string='Issued By', default=lambda self: self.env.user, track_visibility='onchange')
    description = fields.Text(string='Description')
    sale_order_ids = fields.Many2many('sale.order', 'noi_sale_rel', string='Sale Orders')
    purchase_order_ids = fields.Many2many('purchase.order', 'noi_purchase_rel', string='Purchase Orders')
    sale_line_ids = fields.One2many('sale.order.line', 'noi_id', string='Order Lines')
    inspection_date = fields.Datetime(string='Inspection Date')
    inspection_duration = fields.Integer(string='Duration')
    inspection_partner_id = fields.Many2one('res.partner', string='Inspection Location')
    inspector_name = fields.Char(string='Inspector')
    inspector_phone = fields.Char(string='Phone')
    inspector_email = fields.Char(string='Email')
    inspector_company = fields.Char(string='Company')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
