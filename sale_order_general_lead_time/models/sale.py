# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from lxml import etree


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    general_lead_time = fields.Integer(
        string='Lead Time'
    )
    
    weeks_in_report = fields.Boolean('Display weeks in reports')

    def action_update_lead_time(self):
        self.mapped('order_line').update({
            'customer_lead': self.general_lead_time,
        })

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        """Apply general lead time for sale order lines which are not created
        from sale order form view.
        """
        if 'customer_lead' not in vals and 'order_id' in vals:
            sale_order = self.env['sale.order'].browse(vals['order_id'])
            if sale_order.general_lead_time:
                vals['customer_lead'] = sale_order.general_lead_time
        return super().create(vals)
