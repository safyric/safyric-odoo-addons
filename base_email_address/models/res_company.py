# -*- coding: utf-8 -*-

from odoo import models, fields

class ResCompany(models.Model):
    _inherit = "res.company"

    email_sale = fields.Char('Email Sales')
    email_invoicing = fields.Char('Email Invoicing')
