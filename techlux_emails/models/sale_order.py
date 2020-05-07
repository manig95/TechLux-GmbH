from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    # def action_confirm(self):
    #     result = super(SaleOrder, self).action_confirm()
    #     template_id = self.env.ref('techlux_emails.sale_mail_template_sale_confirmation')
    #     if template_id:
    #         for order in self:
    #             template_id.with_context().send_mail(order.id,force_send=True)
    #
    #     return result
