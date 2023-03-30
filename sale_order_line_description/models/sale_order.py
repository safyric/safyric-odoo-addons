# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_long_description = fields.Boolean('Order Line Long Description', help="Is true if the sales order line is long full description.")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    @api.multi
    def get_sale_order_line_multiline_description_sale(self, product):
        res = super(SaleOrderLine,self).get_sale_order_line_multiline_description_sale(product)
        barcode = ""
        if product.barcode:
            barcode = "\nStock Code: " + product.barcode

        if product.description_sale:
            return product.display_name + barcode + "\n" + self._get_sale_order_line_multiline_description_variants().strip(', ') + product.description_sale
        else:
            return product.display_name + barcode + "\n" + self._get_sale_order_line_multiline_description_variants().strip(', ')

        return res

    def _get_sale_order_line_multiline_description_variants(self):
        res1 = super(SaleOrderLine,self)._get_sale_order_line_multiline_description_variants()
        name = ""

        product_attribute_with_is_custom = self.product_custom_attribute_value_ids.mapped('attribute_value_id.attribute_id')

        # attribute_value_with_variants
        for pav in self.product_id.attribute_value_ids.with_context(lang=self.order_id.partner_id.lang or self.env.lang).filtered(
            lambda pav: pav.attribute_id not in product_attribute_with_is_custom and pav.code and pav.code != "0" and pav.code !="00" and pav.code !="000"
        ):
            attribute_id = pav.attribute_id.with_context(lang=self.order_id.partner_id.lang or self.env.lang)
            if self.order_id.is_long_description:
                if pav.attribute_id.description and pav.attribute_id.is_reverse_description == False:
                    name += pav.name + " " + attribute_id.description + ", "
                elif pav.attribute_id.description and pav.attribute_id.is_reverse_description == True:
                    name += attribute_id.description + " " + pav.name + ", "
                else:
                    name += pav.name + ", "
            else:
                name += attribute_id.name + ': ' + pav.name + "\n"

        # no_variant_attribute_value
        for pvav in self.product_no_variant_attribute_value_ids.with_context(lang=self.order_id.partner_id.lang or self.env.lang).filtered(
            lambda pvav: pvav.attribute_id not in product_attribute_with_is_custom):
            attribute_id = pvav.attribute_id.with_context(lang=self.order_id.partner_id.lang or self.env.lang)
            if self.order_id.is_long_description:
                if pvav.attribute_id.description and pvav.attribute_id.is_reverse_description == False:
                    name += pvav.name + " " + attribute_id.description + ", "
                elif pvav.attribute_id.description and pvav.attribute_id.is_reverse_description == True:
                    name += attribute_id.description + " " + pvav.name + ", "
                else:
                    name += pvav.name + ", "
            else:
                name += attribute_id.name + ': ' + pvav.name + "\n"

        # product_custom_attribute_value
        for pacv in self.product_custom_attribute_value_ids:
            if self.order_id.is_long_description:
                if pacv.attribute_value_id.attribute_id.description and pacv.attribute_value_id.attribute_id.is_reverse_description == False:
                    name += (pacv.custom_value or '').strip() + " " + pacv.attribute_value_id.attribute_id.description + ", "
                elif pacv.attribute_value_id.attribute_id.description and pacv.attribute_value_id.attribute_id.is_reverse_description == True:
                    name += pacv.attribute_value_id.attribute_id.description + " " + (pacv.custom_value or '').strip() + ", "
                else:
                    name += (pacv.custom_value or '').strip() + ", "
            else:
                if pacv.custom_value:
                    name += pacv.attribute_value_id.attribute_id.name + \
                    ': ' + pacv.custom_value.strip() + "\n"

        return name

        return res1
