# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero

from odoo.addons import decimal_precision as dp



class QcItpLine(models.Model):

    _name = "qc.itp.line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Inspection and Test Plan Lines"
    _order = "date desc, id desc"

    @api.model
    def _default_employee_id(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    sequence = fields.Integer('Sequence', help="Determine the display order", default=1, index=True)
    name = fields.Char('Activity', readonly=True, required=True, translate=True, copy=False, states={'draft': [('readonly', False)]})
    date = fields.Date(readonly=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)]}, default=fields.Date.context_today, string="Date")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, states={'draft': [('readonly', False)]}, default=_default_employee_id)
    company_id = fields.Many2one('res.company', string='Company', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.company_id)
    description = fields.Text('Description', readonly=True, translate=True, states={'draft': [('readonly', False)]})
    reference_ids = fields.Many2many('qc.itp.ref', 'itp_ref_rel', string='Reference Documents')
    acc_criteria_ids = fields.Many2many('qc.itp.ref', 'itp_acc_rel', string='Acceptance Criteria')
    verify_doc_ids = fields.Many2many('qc.itp.verify.doc', string='Verifying Documents')
    records_ids = fields.Many2many('qc.itp.records', string='Records')
    process_id = fields.Many2one('qc.itp.proc', string='Process')
    insp_level1_id = fields.Many2one('qc.itp.insp.level', string='L1')
    insp_level2_id = fields.Many2one('qc.itp.insp.level', string='L2')
    insp_level3_id = fields.Many2one('qc.itp.insp.level', string='L3')
    insp_level4_id = fields.Many2one('qc.itp.insp.level', string='L4')
    insp_level5_id = fields.Many2one('qc.itp.insp.level', string='L5')
    insp_level6_id = fields.Many2one('qc.itp.insp.level', string='L6')
    notes = fields.Text('Notes', translate=True)
    attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('submitted', 'Submitted'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
        ('done', 'Done')
    ], compute='_compute_state', string='Status', copy=False, index=True, readonly=True, store=True, help="Status of the plan")
    plan_id = fields.Many2one('qc.itp', string="ITP", readonly=True, copy=False)

    @api.depends('plan_id', 'plan_id.state')
    def _compute_state(self):
        for line in self:
            if not line.plan_id or line.plan_id.state == 'draft':
                line.state = "draft"
            elif line.plan_id.state == "rejected":
                line.state = "rejected"
            elif line.plan_id.state == 'submitted':
                line.state = 'submitted'
            elif line.plan_id.state == "approved":
                line.state = "approved"
            else:
                line.state = "done"

    @api.multi
    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'qc.itp.line'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for line in self:
            line.attachment_number = attachment.get(line.id, 0)

    # ----------------------------------------
    # ORM Overrides
    # ----------------------------------------

    @api.multi
    def unlink(self):
        for line in self:
            if line.state in ['done', 'approved']:
                raise UserError(_('You cannot delete a posted or approved plan line.'))
        return super(QcItpLine, self).unlink()


    # ----------------------------------------
    # Actions
    # ----------------------------------------

    @api.multi
    def action_view_line(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'qc.itp',
            'target': 'current',
            'res_id': self.plan_id.id
        }

    @api.multi
    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'qc.itp.line'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'qc.itp.line', 'default_res_id': self.id}
        return res


class QcItp(models.Model):
    """
    """
    _name = "qc.itp"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Inspection and Test Plan"
    _order = "date desc, id desc"


    name = fields.Char(readonly=True)
    date = fields.Date(default=fields.Date.context_today, string="Date")
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    sale_order_ids = fields.Many2many('sale.order', string='Sales Order')
    purchase_order_ids = fields.Many2many('purchase.order','qc_itp_purchase_rel', string='Purchase Order')
    project_name = fields.Char('Project Name', translate=True)
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    enduser_id = fields.Many2one('res.partner', string='End-user')
    tpi_id = fields.Many2one('res.partner', string="TPIA")
    plan_line_ids = fields.One2many('qc.itp.line', 'plan_id', string='Plan Lines', states={'approve': [('readonly', True)]}, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'In review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Completed')
    ], string='Status', index=True, readonly=True, track_visibility='onchange', copy=False, default='draft', required=True, help='Plan Lines')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1))
    user_id = fields.Many2one('res.users', 'Manager', readonly=True, copy=False, states={'draft': [('readonly', False)]}, track_visibility='onchange', oldname='responsible_id')
    company_id = fields.Many2one('res.company', string='Company', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.company_id)
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')

    @api.constrains('plan_line_ids', 'employee_id')
    def _check_employee(self):
        for plan in self:
            employee_ids = plan.plan_line_ids.mapped('employee_id')
            if len(employee_ids) > 1 or (len(employee_ids) == 1 and employee_ids != plan.employee_id):
                raise ValidationError(_('You cannot add plan of another employee.'))


    @api.model
    def create(self, vals):
        self.with_context(mail_create_nosubscribe=True)
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'qc.itp') or ''
        return super(QcItp, self).create(vals)

    @api.multi
    def _compute_attachment_number(self):
        for plan in self:
            plan.attachment_number = sum(plan.plan_line_ids.mapped('attachment_number'))
