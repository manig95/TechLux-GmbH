from odoo import api, fields, models, _

class SendMailTemplate(models.TransientModel):
    _name = "send.preview.mail.wizard"

    @api.model
    def _get_records(self):
        """ Return Records of particular Email Template's Model """
        template_id = self._context.get('active_id')
        default_res_id = self._context.get('default_res_id')
        if not template_id:
            return []
        template = self.env['mail.template'].browse(int(template_id))
        records = self.env[template.model_id.model].search([], order="id desc", limit=50)
        records |= records.browse(default_res_id)
        return records.name_get()

    @api.model
    def default_get(self, fields):
        result = super(SendMailTemplate, self).default_get(fields)

        if 'res_id' in fields and not result.get('res_id'):
            records = self._get_records()
            result['res_id'] = records and records[0][0] or False  # select first record as a Default
        if self._context.get('template_id') and 'model_id' in fields and not result.get('model_id'):
            result['model_id'] = self.env['mail.template'].browse(self._context['template_id']).model_id.id
        return result

    res_id = fields.Selection(_get_records, 'Sample Document')
    send_mail_to = fields.Char("Send Mail To")
    model_id = fields.Many2one('ir.model', 'Applies to', help="The type of document this template can be used with")

    def send_preview_mail_action(self):
        if self._context.get('active_id'):
            template_id = self.env['mail.template'].browse(int(self._context.get('active_id')))
            prv_email_to = template_id.email_to
            prv_partner_to = template_id.partner_to
            template_id.write({'email_to': self.send_mail_to,'partner_to':False})
            template_id.send_mail(int(self.res_id), force_send=True)
            template_id.write({'email_to': prv_email_to,'partner_to':prv_partner_to})
        return True
