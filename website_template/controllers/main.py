from odoo.addons.mass_mailing.controllers.main import MassMailController
import random
import logging
from odoo import fields, http, tools, _
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import UserError
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import Forbidden, NotFound

_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        Partner = request.env['res.partner']
        if mode[0] == 'new':
            checkout.update({'name': all_values.get('name') + " " + all_values.get('lastname')})
            partner_id = Partner.sudo().create(checkout).id
        elif mode[0] == 'edit':
            partner_id = int(all_values.get('partner_id', 0))
            if partner_id:
                # double check
                order = request.website.sale_get_order()
                shippings = Partner.sudo().search([("id", "child_of", order.partner_id.commercial_partner_id.ids)])
                if partner_id not in shippings.mapped('id') and partner_id != order.partner_id.id:
                    return Forbidden()
                Partner.browse(partner_id).sudo().write(checkout)
        return partner_id



class AuthSignupHome(Home):
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang

        values.update({
            'title': qcontext.get("title"),
            'name': qcontext.get("name")+" " +qcontext.get("lastname"),
            'dob': qcontext.get("dob"),
        })

        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

class WebsiteSaleForm(WebsiteForm):
    def _get_mandatory_billing_fields(self):
        return ["name", "email","confirm_email", "street", "city", "country_id","lastname","zip"]

    def _get_mandatory_shipping_fields(self):
        return ["name", "email","confirm_email", "street", "city", "country_id","lastname","zip"]


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
        # return True


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
