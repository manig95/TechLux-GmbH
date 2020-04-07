from odoo import models

class Picking(models.Model):
    _inherit = 'stock.picking'


    def _send_confirmation_email(self):
        for stock_pick in self.filtered(lambda p: p.company_id.stock_move_email_validation and p.picking_type_id.code == 'outgoing'):
            delivery_template_id = stock_pick.company_id.stock_mail_confirmation_template_id
            delivery_template_id.with_context().send_mail(stock_pick.id, force_send=True)