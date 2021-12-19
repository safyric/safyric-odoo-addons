# -*- coding: utf-8 -*-

from odoo import fields, models

class DeliveryPlace(models.Model):
    _name = "stock.delivery.place"
    _description = "Stock Delivery Place"

    name = fields.Char(
        'Name', required=True, translate=True,
        help="Delivery places are generally used with Incoterms to distinguish responsibilities.")
    code = fields.Char(
        'Code', required=True,
        help="Ports Standard Code")
    active = fields.Boolean(
        'Active', default=True,
        help="By unchecking the active field, you may hide a delivery point you will not use.")
