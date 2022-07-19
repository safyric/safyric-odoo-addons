from odoo import api, fields, models

class SaleOrderOption(models.Model):
    _inherit = "sale.order.option"

    customer_lead = fields.Float(
        'Delivery Lead Time', required=True, default=0.0,
        help="Number of days between the order confirmation and the shipping of the products to the customer")
