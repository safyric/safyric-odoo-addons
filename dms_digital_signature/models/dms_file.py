# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import re
from odoo import _, api, fields, models


class DmsFile(models.Model):
    _inherit = "dms.file"


    signed_doc = fields.Binary(attachment=False, string='Signed Document', realonly=True)
    signed_doc_name = fields.Char('Filename')


    @api.onchange("content", "signed_doc")
    def onchange_binaryfields(self):
        if self.name:
            content_name = re.sub(' +', ' ', str(self.name).replace(' - ', '')).replace(' ', '_')
            self.name = content_name
        if self.signed_doc_name:
            signed_doc_name = re.sub(' +', ' ', str(self.signed_doc_name).replace(' - ', '')).replace(' ', '_')
            self.signed_doc_name = signed_doc_name
