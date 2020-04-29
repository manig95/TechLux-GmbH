import random
from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval


class SaleCouponProgram(models.Model):
    _inherit = 'sale.coupon.program'

    signup_coupon= fields.Boolean("Is signup Coupon?")



class SaleCoupon(models.Model):
    _inherit = 'sale.coupon'

    code = fields.Char(required=True, readonly=True)


class SaleCouponGenerate(models.TransientModel):
    _inherit = 'sale.coupon.generate'


    def generate_coupon(self):
        """Generates the number of coupons entered in wizard field nbr_coupons
        """
        program = self.env['sale.coupon.program'].browse(self.env.context.get('active_id'))

        if program.signup_coupon:
            code = "SIGNUP" + str(random.getrandbits(16))
        else:
            code = str(random.getrandbits(64))

        vals = {'program_id': program.id,'code':code}

        if self.generation_type == 'nbr_coupon' and self.nbr_coupons > 0:
            for count in range(0, self.nbr_coupons):
                self.env['sale.coupon'].create(vals)

        if self.generation_type == 'nbr_customer' and self.partners_domain:
            for partner in self.env['res.partner'].search(safe_eval(self.partners_domain)):
                vals.update({'partner_id': partner.id})
                coupon = self.env['sale.coupon'].create(vals)
                subject = '%s, a coupon has been generated for you' % (partner.name)
                template = self.env.ref('sale_coupon.mail_template_sale_coupon', raise_if_not_found=False)
                if template:
                    template.send_mail(coupon.id, email_values={'email_to': partner.email, 'email_from': self.env.user.email or '', 'subject': subject,})

