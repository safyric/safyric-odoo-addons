# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero

from odoo.addons import decimal_precision as dp



class QcMtcLine(models.Model):

    _name = "qc.mtc.line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "MTC Lines"


    sequence = fields.Integer('Sequence', help="Determine the display order", default=1, index=True)
    name = fields.Char('Heat Code', required=True)
    material = fields.Many2one('qc.mtc.materials', string='Material', required=True)
    mtc_id = fields.Many2one('qc.mtc', string="MTC")
    company_id = fields.Many2one('res.company', string='Company', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.company_id)
    inspection_id = fields.Many2one('qc.inspection', string='Inspection')
    c = fields.Float('C', digits=(12,3))
    mn = fields.Float('Mn', digits=(12,3))
    p = fields.Float('P', digits=(12,3))
    s = fields.Float('S', digits=(12,3))
    si = fields.Float('Si', digits=(12,3))
    cu = fields.Float('Cu', digits=(12,3))
    ni = fields.Float('Ni', digits=(12,3))
    cr = fields.Float('Cr', digits=(12,3))
    mo = fields.Float('Mo', digits=(12,3))
    v = fields.Float('V', digits=(12,3))
    nb = fields.Float('Nb', digits=(12,3))
    n = fields.Float('N', digits=(12,3))
    ti = fields.Float('Ti', digits=(12,3))
    co = fields.Float('Co', digits=(12,3))
    al = fields.Float('Al', digits=(12,3))
    ce = fields.Float('CE', digits=(12,2), compute='_compute_ce')

    @api.depends('c', 'si', 'mn')
    def _compute_ce(self):
        for rec in self:
            ce = self.c + (self.si+self.mn)/3
            rec.ce = ce

    notes = fields.Text('Notes', translate=True)

    tensile_strength = fields.Integer('Tensile Strength')
    yield_strength = fields.Integer('Yield Strength')
    elongation = fields.Integer('Elongation')
    reduction_of_area = fields.Integer('Reduction of Area')
    impact_energy_1 = fields.Integer('Impact Energy 1')
    impact_energy_2 = fields.Integer('Impact Energy 2')
    impact_energy_3 = fields.Integer('Impact Energy 3')
    impact_temperature = fields.Integer('Test Temperature')
    hardness = fields.Integer('Hardness')
    heat_treatment = fields.Char('Heat Treatment')


class QcMtcMaterials(models.Model):
    _name = "qc.mtc.materials"
    _description = "Materials"

    name = fields.Char('Material')
    impact_test = fields.Boolean('Impact Test', default=False)

class QcMtcTest(models.Model):
    _name = "qc.mtc.test"
    _description = "Tests"

    name = fields.Selection([
        ('shell', 'Shell'),
        ('seat_hp', 'Seat (H.P.)'),
        ('seat_lp', 'Seat (L.P.)'),
        ('backseat', 'Backseat')
    ], default='shell', string='Type')
    pressure = fields.Integer('Pressure')
    pressure_uom = fields.Many2one('uom.uom', string='Pressure UOM')
    duration = fields.Integer('Duration')
    duration_uom = fields.Many2one('uom.uom', string='Duration UOM')
    inspection_id = fields.Many2one('qc.inspection', string='Inspection')
    result = fields.Selection([('acc', 'Acceptable'), ('rej', 'Rejected')], default='acc', string='Result')
    mtc_id = fields.Many2one('qc.mtc', string='MTC')


class QcMtcMatConfig(models.Model):
    _name = "qc.mtc.heat.code"
    _description = "MTC Heat Code"

    body = fields.Char('Body', required=True)
    bonnet_cover = fields.Char('Bonnet/Cover')
    disc_ball_gate = fields.Char('Disc/Ball/Gate')
    seat = fields.Char('Seat')
    stem = fields.Char('Stem')
    lot_ids = fields.Many2many('stock.production.lot', 'stock_prod_lot_mtc_mat_rel', string='Lot/Serial Number')
    product_id = fields.Many2one('product.product', string='Product', related='mtc_id.product_id')
    mtc_id = fields.Many2one('qc.mtc', string='MTC')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s - %s' % (record.lot_ids[0], record.body)))
        return result


class QcItp(models.Model):
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
    project_name = fields.Char('Project Name', translate=True)
    test_ids = fields.One2many('qc.mtc.test', 'mtc_id', string='Test')
    test_std = fields.Selection([('598', 'API Std 598'), ('6d', 'API Spec 6D')], default='598', string='Test Std')
    mtc_heat_code_ids = fields.One2many('qc.mtc.heat.code', 'mtc_id', string='Heat Code', copy=False)
    mtc_line_ids = fields.One2many('qc.mtc.line', 'mtc_id', string='MTC Lines', copy=False)
    insp_visual = fields.Selection([('acc', 'Acceptable'), ('rej', 'Rejected')], default='acc', string='Visual')
    insp_dimensional = fields.Selection([('acc', 'Acceptable'), ('rej', 'Rejected')], default='acc', string='Dimensional')
    insp_functional = fields.Selection([('acc', 'Acceptable'), ('rej', 'Rejected')], default='acc', string='Functional')
    insp_marking = fields.Selection([('acc', 'Acceptable'), ('rej', 'Rejected')], default='acc', string='Marking')
    insp_marking_std = fields.Selection([('sp25', 'MSS SP-25'), ('other', 'Other')], default='sp25', string='Marking Std')
    notes = fields.Text('Notes')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'In review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Completed')
    ], string='Status', index=True, readonly=True, track_visibility='onchange', copy=False, default='draft', required=True, help='Plan Lines')
    user_id = fields.Many2one('res.users', 'User', copy=False, track_visibility='onchange')
    company_id = fields.Many2one('res.company', string='Company', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.company_id)


    @api.model
    def create(self, vals):
        self.with_context(mail_create_nosubscribe=True)
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'qc.mtc') or ''
        return super(QcItp, self).create(vals)

    @api.multi
    @api.onchange('sale_line_id')
    def sale_line_id_change(self):
        vals = {}
        if self.sale_line_id:
            product_id = self.product_id
            description = self.product_id.display_name
            quantity = self.sale_line_id.product_uom_qty
            lot_ids = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id), ('sale_order_ids', 'in', [self.sale_order_id.id])])
            item_tag = str(self.sale_line_id.sequence)
            if self.sale_line_id.item:
                item_tag += '/' + self.sale_line_id.item
        else:
            product_id = False
            description = False
            quantity = False
            lot_ids = False
            item_tag = False
        vals.update({'product_id': product_id, 'description': description, 'quantity': quantity, 'lot_ids': lot_ids, 'item_tag': item_tag})
        self.update(vals)


    @api.multi
    @api.onchange('lot_ids')
    def lot_ids_onchange(self):
        quantity = len(self.lot_ids)
        if self.quantity != quantity:
            self.update({'quantity': quantity})
