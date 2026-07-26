# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero
from odoo.tools.safe_eval import safe_eval
from odoo.addons import decimal_precision as dp



class QcMtcLine(models.Model):

    _name = "qc.mtc.line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "MTC Lines"


    sequence = fields.Integer('Sequence', help="Determine the display order", default=1, index=True)
    name = fields.Char('Heat Code', required=True)
    material_id = fields.Many2one('qc.mtc.material', string='Material', required=True)
    mtc_id = fields.Many2one('qc.mtc', string="MTC", ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.company_id)
    inspection_id = fields.Many2one('qc.inspection', string='Inspection')
    notes = fields.Text('Notes', translate=True)

    @api.onchange('inspection_id')
    def _onchange_inspection_id(self):
        for rec in self:
            rec.name = rec.inspection_id.heat_code
            rec.material_id = rec.inspection_id.material_id


class QcMtcMaterial(models.Model):
    _name = "qc.mtc.material"
    _description = "Material"

    name = fields.Char('Material', required=True)
    short_name = fields.Char('Short Name')
    impact_test = fields.Boolean('Impact Test', default=False)

class QcMtcPart(models.Model):
    _name = 'qc.mtc.part'
    _description = 'Parts'

    name = fields.Char('Name', translate=True)

class QcMtcHeat(models.Model):
    _name = "qc.mtc.heat"
    _description = "MTC Heat Code"

    name = fields.Char('Heat Code', required=True)
    lot_ids = fields.Many2many('stock.production.lot', string='Lot/Serial Numbers',  required=True)
    lot_name = fields.Char('Lot/Serial Numbers')
    part_id = fields.Many2one('qc.mtc.part', string='Part Name', required=True)
    mtc_line_id = fields.Many2one('qc.mtc.line', string='MTC Line', required=True)
    material_id = fields.Many2one('qc.mtc.material', string='Material', related='mtc_line_id.material_id', required=True)
    product_id = fields.Many2one('product.product', string='Product', related='mtc_id.product_id')
    mtc_id = fields.Many2one('qc.mtc', string='MTC', ondelete='cascade')


    @api.onchange('mtc_line_id')
    def _onchange_mtc_line_id(self):
        for rec in self:
            rec.name = rec.mtc_line_id.name

    @api.onchange('lot_ids')
    def _onchange_lot_ids(self):
        for rec in self:
            lots = rec.lot_ids.mapped('name')
            if lots:
                if any(not i.isdigit() for i in lots):
                    rec.lot_name = ",".join(lots)
                    return

                if len(lots) == 1:
                    rec.lot_name = lots[0]
                    return

                nums = sorted(set([int(x) for x in lots]))
                result = []
                start = nums[0]
                prev = nums[0]

                for i in range(1, len(nums)):
                    if nums[i] == prev + 1:
                        prev = nums[i]
                    else:
                        if start == prev:
                            result.append(str(start))
                        else:
                            result.append(f"{start}-{prev}")
                        start = nums[i]
                        prev = nums[i]

                if start == prev:
                    result.append(str(start))
                else:
                    result.append(f"{start}-{prev}")

                rec.lot_name = ', '.join(map(str, result))

            else:
                rec.lot_name = ''

class QcMtc(models.Model):
    """
    """
    _name = "qc.mtc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "MTC"
    _order = "date desc, id desc"


    name = fields.Char(readonly=True)
    date = fields.Date(default=fields.Date.context_today, string="Issue Date")
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    sale_order_id = fields.Many2one('sale.order', string='Sales Order', required=True)
    sale_line_id = fields.Many2one('sale.order.line', string='Order Line')
    product_id = fields.Many2one('product.product', string='Product', related='sale_line_id.product_id')
    item_tag = fields.Char('Line Item/Tag Number')
    description = fields.Text('Description', required=True)
    quantity = fields.Integer('Quantity', required=True)
    lot_ids = fields.One2many('stock.production.lot', 'mtc_id', string='Lot/Serial Number')
    lot_name = fields.Char('Lot/Serial Number')
    project_name = fields.Char('Project Name', translate=True)
    report_show_vendor = fields.Boolean('Show Vendor in Report?', default=False)
    inspection_ids = fields.Many2many('qc.inspection', string='Inspection and Tests')
    mtc_heat_ids = fields.One2many('qc.mtc.heat', 'mtc_id', string='Heat Codes', copy=False)
    mtc_line_ids = fields.One2many('qc.mtc.line', 'mtc_id', string='MTC Lines', copy=False)
    notes = fields.Text('Notes', translate=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'In review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Completed')
    ], string='Status', index=True, readonly=True, track_visibility='onchange', copy=False, default='draft', required=True, help='Plan Lines')
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user, track_visibility='onchange')
    company_id = fields.Many2one('res.company', string='Company', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.company_id)


    vendor_id = fields.Many2one('res.partner', string='Vendor')

    @api.model
    def _default_statement(self):
        return self.env.user.company_id.mtc_statement or ''

    statement = fields.Text('Statement', default=_default_statement, translate=True)

    @api.model
    def create(self, vals):
        self.with_context(mail_create_nosubscribe=True)
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'qc.mtc') or ''
        return super(QcMtc, self).create(vals)

    @api.multi
    @api.onchange('sale_line_id')
    def sale_line_id_change(self):
        vals = {}
        lot_ids = []
        partner_id = []
        notes = ''
        if self.sale_line_id:
            purchase_line_id = self.env['purchase.order.line'].search([('sale_line_id', '=', self.sale_line_id.id)], limit=1)
            product_id = self.product_id
            description = self.product_id.display_name
            quantity = self.sale_line_id.product_uom_qty
            lot_ids = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id), ('sale_order_ids', 'in', [self.sale_order_id.id])])
            item_tag = str(self.sale_line_id.sequence)
            if self.sale_line_id.item:
                item_tag += '/' + self.sale_line_id.item

            attribute_values = self.product_id.attribute_value_ids.filtered(lambda r: not r.is_custom and r.attribute_id.show_on_mtc).mapped('name')
            if attribute_values:
                notes = 'Reference Standards/Specifications: ' + ', '.join(attribute_values)
            else:
                notes = ''

        else:
            purchase_line_id = False
            product_id = False
            description = False
            quantity = False
            lot_ids.append((5,0,0))
            item_tag = False


        if purchase_line_id:
            partner_id = purchase_line_id.partner_id

        vals.update({'product_id': product_id, 'description': description, 'quantity': quantity, 'lot_ids': lot_ids, 'item_tag': item_tag, 'mtc_heat_ids': False, 'vendor_id': partner_id, 'notes': notes})
        self.update(vals)


    @api.multi
    @api.onchange('lot_ids')
    def lot_ids_onchange(self):
        quantity = len(self.lot_ids)
        if self.quantity != quantity:
            self.update({'quantity': quantity})

        lots = self.lot_ids.mapped('name')
        if len(lots) == 1:
            self.lot_name = lots[0]
            return

        if any(not i.isdigit() for i in lots):
            lot_name = ', '.join(lots)
        else:
            nums = [int(i) for i in sorted(lots)]
            ranges = sum((list(t) for t in zip(nums, nums[1:]) if t[0]+1 != t[1]), [])
            iranges = iter(nums[0:1] + ranges + nums[-1:])
            lot_name = ', '.join([str(n) + '-' + str(next(iranges)) for n in iranges])
        self.lot_name = lot_name
