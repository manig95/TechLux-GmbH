from odoo import api, fields, models


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    payment_notes = fields.Html("Payment Notes", translate=True)