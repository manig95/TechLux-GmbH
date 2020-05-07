
from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = "account.move"

    def print_invoice(self):
        self.ensure_one()
        return self.env.ref('account.account_invoices').report_action(self)