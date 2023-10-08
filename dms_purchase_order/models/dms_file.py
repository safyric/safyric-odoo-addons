# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import re
from odoo import _, api, fields, models


class DmsFile(models.Model):
    _inherit = "dms.file"


    purchase_id = fields.Many2one('purchase.order', string='Purchase Order')
    to_print = fields.Boolean('To Print', default=False)
