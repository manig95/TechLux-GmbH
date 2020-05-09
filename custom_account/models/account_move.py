
from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = "account.move"

    def print_invoice(self):
        self.ensure_one()
        return self.env.ref('account.account_invoices').report_action(self)

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        if vals.get("invoice_origin"):
            picking = self.env["stock.picking"].search([('origin', '=', vals.get("invoice_origin")), ('state', '!=', 'cancel')], limit=1)
            if picking:
                res.delivery_no = picking.name
        return res
