from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
from odoo.addons.mass_mailing.controllers.main import MassMailController

class MassMailController(MassMailController):

    @http.route('/website_mass_mailing/subscribe', type='json', website=True, auth="public")
    def subscribe(self, list_id, email, **post):
        ContactSubscription = request.env['mailing.contact.subscription'].sudo()
        Contacts = request.env['mailing.contact'].sudo()
        name = ''
        if Contacts:
            name, email = Contacts.get_name_email(email)

        subscription = ContactSubscription.search([('list_id', '=', int(list_id)), ('contact_id.email', '=', email)], limit=1)
        if not subscription:
            # inline add_to_list as we've already called half of it
            contact_id = Contacts.search([('email', '=', email)], limit=1)
            if not contact_id:
                contact_id = Contacts.create({'name': name, 'email': email})
            ContactSubscription.create({'contact_id': contact_id.id, 'list_id': int(list_id)})
        elif subscription.opt_out:
            subscription.opt_out = False
        # add email to session
        request.session['mass_mailing_email'] = email
        mass_mailing_list = request.env['mailing.list'].sudo().browse(list_id)
        return {'toast_content': mass_mailing_list.toast_content}


class WebsiteCoupon(http.Controller):

    @http.route(['/generate_promo_code'], type='http', auth="public", csrf=False, website=True)
    def send_category_enquiry(self, **post):
        user = request.env['res.users'].browse(SUPERUSER_ID)
        if post.get('name') and post.get('email_id') and post.get('comment'):
            values = {
                'record_name': post.get('name'),
                'model': 'mail.message',
                'message_type': 'email',
                'reply_to': post.get('mail_id')
            }
            rec_id = request.env['mail.message'].sudo().create(values)
            template_id = request.env.ref('website_product_category.website_enquiry_mail_template')
            print
            post, '========================='
            if template_id:
                template_id.sudo().with_context({'mail_id': post.get('email_id'), 'name': post.get('name'), 'comments': post.get('comment'), 'search_string': post.get("search_string")}).send_mail(rec_id.id, force_send=True)
            return 'mail_sent'
        else:
            return 'mail_not_sent'
