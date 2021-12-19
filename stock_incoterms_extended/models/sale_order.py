# -*- coding: utf-8 -*-

from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_place = fields.Many2one(
        'stock.delivery.place', 'Incoterms Port',
        help="Incoterms port")
    incoterm = fields.Many2one(
        'account.incoterms', 'Incoterms',
        help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
