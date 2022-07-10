# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    vendor_id = fields.Many2one('product.supplierinfo', 'Vendor')
    is_route = fields.Boolean('Is Route', defualt=False)
    product_tmpl_id = fields.Many2one(related='product_id.product_tmpl_id',
                                      string='Product Template',
                                      store=True)

    @api.multi
    @api.onchange('route_id')
    def _onchange_route_id(self):
        if self.route_id:
            self.is_route = True


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _make_po_select_supplier(self, values, suppliers):
        """ Method intended to be overridden by customized
        modules to implement any logic in the
            selection of supplier.
        """
        if values.get('route_ids'):
            so = self.env['sale.order.line'].browse(values.get('sale_line_id'))
            supplier = so.vendor_id or suppliers[0]

            return supplier
        else:
            return super(ProcurementRule, self)\
                ._make_po_select_supplier(values, suppliers)
