from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"
    
    cod_payment = fields.Boolean(string='COD Payment')
    payment_term_id = fields.Many2one("account.payment.term","Payment Term")
    
class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _set_transaction_pending(self):
        # Override of '_set_transaction_pending' in the 'payment' module
        # to sent the quotations automatically.
        super(PaymentTransaction, self)._set_transaction_pending()

        for record in self:
            sales_orders = record.sale_order_ids.filtered(lambda so: so.state in ['draft', 'sent'])
            sales_orders.filtered(lambda so: so.state == 'draft').with_context(tracking_disable=True).write({'state': 'sent'})

            if record.acquirer_id.provider == 'transfer':
                for so in record.sale_order_ids:
                    so.reference = record._compute_sale_order_reference(so)
            # send order confirmation mail
            # sales_orders._send_order_confirmation_mail()