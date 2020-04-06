from odoo import api, fields, models, _

class MailTemplate(models.Model):
    _inherit = "mail.template"

    def send_preview_mail(self):
        vals = ({'default_model_id':self.model_id.id})
        return {
            'name': "Send Mail Preview",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'send.preview.mail.wizard',
            'target': 'new',
            'context': vals,
        }
