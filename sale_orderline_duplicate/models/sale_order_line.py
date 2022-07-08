# -*- coding: utf-8 -*-
from odoo import models, api
from datetime import datetime
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def dup_line(self):
        max_seq = max(line.sequence for line in self.order_id.order_line)
        self.copy({'order_id': self.order_id.id, 'sequence': max_seq + 1})
