from odoo import api, models, fields, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class SaleLine(models.Model):
    _inherit = 'sale.order.line'


    # sequence_ref = fields.Integer("Pos.",compute='_sequence_ref')
    product_code = fields.Char("Article Number/EAN Code")

    @api.onchange('product_id')
    def product_id_on_change(self):
        if self.product_id:
            if self.product_id.barcode:
                self.product_code = self.product_id.barcode


    def _prepare_invoice_line(self):
        res = super(SaleLine, self)._prepare_invoice_line()  # <-- ensure_one()
        res.update({
                'product_code': self.product_code,
            })
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_gateway_id = fields.Many2one("payment.acquirer", string="Payment Method")
    state = fields.Selection(selection_add=[('paid', 'Direct Orders'), ('unpaid', 'Indirect Order')])
    paid_order = fields.Boolean("Paid Order")
    unpaid_order = fields.Boolean("Unpaid Orders")
    our_ref = fields.Char("Our Reference")
    client_ref = fields.Char("Your Reference")


    def _website_product_id_change(self, order_id, product_id, qty=0):
        res = super(SaleOrder, self)._website_product_id_change(order_id, product_id, qty=qty)
        res['product_code']= self.env['product.template'].browse(product_id).article_number
        return res


    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False

        if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('techlux_emails.sale_mail_template_sale_confirmation_new'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('techlux_emails.sale_mail_template_sale_confirmation_new', raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('techlux_emails.sale_mail_template_sale_confirmation_new', raise_if_not_found=False)

        return template_id


    def action_quotation_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_template(template.lang, 'sale.order', self.ids[0])
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            # 'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def _send_order_confirmation_mail(self):
        template_id = self._find_mail_template(force_confirmation_template=True)
        if template_id:
            template = self.env["mail.template"].browse(template_id)
            for order in self:
                template.send_mail(order.id,force_send=True)


    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        template_id = self.env.ref('techlux_emails.sale_mail_template_sale_confirmation_final')
        if template_id:
            template_id.send_mail(self.id,force_send=True)

        stock_picking_id = self.env['stock.picking'].search([('origin', '=', self.name)], limit=1)
        if stock_picking_id:
            for rec in self.order_line:
                for line in stock_picking_id.move_ids_without_package:
                    if rec.product_id == line.product_id:
                        line.product_code = rec.product_code
        return result



