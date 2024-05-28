# Copyright (C) 2022 PESOL (<http://www.camptocamp.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import fields, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    print_report_name = fields.Char(translate=True)
