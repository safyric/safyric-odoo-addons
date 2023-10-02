# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class DmsFile(models.Model):
    _inherit = "dms.file"


    signed_doc = fields.Binary(attachment=False, string='Signed Document', realonly=True)
    signed_doc_name = fields.Char('Filename')
