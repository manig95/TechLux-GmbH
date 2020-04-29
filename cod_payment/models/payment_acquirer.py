from odoo import fields, models, api

class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"
    
    cod_payment = fields.Boolean(string='COD Payment')
    
class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _set_transaction_pending(self):

        '''Move the transaction to the pending state(e.g. Wire Transfer).'''
        allowed_states = ('draft',)
        target_state = 'pending'
        (tx_to_process, tx_already_processed, tx_wrong_state) = self._filter_transaction_state(allowed_states, target_state)
        for tx in tx_already_processed:
            _logger.info('Trying to write the same state twice on tx (ref: %s, state: %s' % (tx.reference, tx.state))
        for tx in tx_wrong_state:
            _logger.warning('Processed tx with abnormal state (ref: %s, target state: %s, previous state %s, expected previous states: %s)' % (tx.reference, target_state, tx.state, allowed_states))

        tx_to_process.write({
            'state': target_state,
            'date': fields.Datetime.now(),
            'state_message': '',
        })
        tx_to_process._log_payment_transaction_received()
        # Override of '_set_transaction_pending' in the 'payment' module
        # to sent the quotations automatically.

        for record in self:
            sales_orders = record.sale_order_ids.filtered(lambda so: so.state in ['draft', 'sent'])
            sales_orders.filtered(lambda so: so.state == 'draft').with_context(tracking_disable=True).write({'state': 'sent'})

            if record.acquirer_id.provider == 'transfer':
                for so in record.sale_order_ids:
                    so.reference = record._compute_sale_order_reference(so)
            # send order confirmation mail
            if not record.acquirer_id.cod_payment == True:
                sales_orders._send_order_confirmation_mail()