from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
from odoo.addons.mass_mailing.controllers.main import MassMailController
import random

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
        return True


class WebsiteCoupon(http.Controller):

    @http.route(['/generate_signup_coupon'], type='http', auth="public", csrf=False, website=True)
    def send_category_enquiry(self, **post):
        # sale_search = request.env["sale.order"].sudo().search([('partner_id.email','=',post.get('email_id'),('state','!=','cancel'))])
        # if sale_search:
        #     return "You already availed this offer!"
        # else:
        program = request.env["sale.coupon.program"].sudo().search([('signup_coupon','=',True)],limit=1)
        if program:
            if program.signup_coupon:
                code = "SIGNUP" + str(random.getrandbits(16))
            else:
                code = str(random.getrandbits(64))
            vals = {'program_id': program.id, 'code': code}
            coupon = request.env['sale.coupon'].sudo().create(vals)
            return coupon.code
