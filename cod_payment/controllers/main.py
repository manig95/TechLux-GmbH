# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import requests
from odoo import http, tools, _
from odoo.http import request
from requests import get
from odoo.addons.payment.controllers.portal import PaymentProcessing

class PaymentProcessing(http.Controller):

    @staticmethod
    def get_payment_transaction_ids():
        # return the ids and not the recordset, since we might need to
        # sudo the browse to access all the record
        # I prefer to let the controller chose when to access to payment.transaction using sudo
        return request.session.get("__payment_tx_ids__", [])
        
    @http.route(['/payment/process'], type="http", auth="public", website=True, sitemap=False)
    def payment_status_page(self, **kwargs):
        # When the customer is redirect to this website page,
        # we retrieve the payment transaction list from his session
        tx_ids_list = self.get_payment_transaction_ids()
        payment_transaction_ids = request.env['payment.transaction'].sudo().browse(tx_ids_list).exists()

        render_ctx = {
            'payment_tx_ids': payment_transaction_ids.ids,
        }
        if payment_transaction_ids:
            pay_tx = max(payment_transaction_ids.ids)
            pay_tx = request.env['payment.transaction'].sudo().browse(pay_tx)
            if pay_tx.state == 'pending':
                if pay_tx.acquirer_id.cod_payment == True:
                    order = request.website.sudo().sale_get_order()
                    pay_tx.state = 'done'
                    order.sudo().action_confirm()
                    # return request.redirect('/shop/confirmation')
        return request.render("payment.payment_process_page", render_ctx)