# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    description = fields.Char('Description', translate=True)
    is_reverse_description = fields.Boolean('Reverse Description', help="Is true if the attribute name is ahead of attribute value.")

class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    short_name = fields.Char(string='Short Name', translate=True)
    description = fields.Text(string='Description', translate=True)

    @api.multi
    def _variant_name(self, variable_attributes):
        res = super(ProductAttributeValue,self)._variant_name(variable_attributes)
        return ", ".join([str(v.short_name) for v in self if v.short_name and v.attribute_id in variable_attributes])
        return res
