from odoo import fields, models, api, _


class Sale(models.Model):
    _inherit = 'sale.order'

    payment_gateway_id = fields.Many2one("payment.acquirer", string="Payment Method")
    state = fields.Selection(selection_add=[('paid', 'Direct Orders'), ('unpaid', 'Indirect Order')])

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False

        # if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
        #     template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_confirmation_template'))
        #     template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
        #     if not template_id:
        #         template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.mail_template_sale_confirmation', raise_if_not_found=False)
        # if not template_id:
        template_id = self.env['ir.model.data'].xmlid_to_res_id('techlux_emails.sale_mail_template_sale_confirmation', raise_if_not_found=False)

        return template_id

    def confirm_paid_order(self):
        self.state = "paid"

    def action_confirm(self):
        result = super(Sale, self).action_confirm()
        template_id = self.env.ref('techlux_emails.sale_mail_template_sale_confirmation_final')
        if template_id:
            for order in self:
                template_id.with_context().send_mail(order.id,force_send=True)

        return result
