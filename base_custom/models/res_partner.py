from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    dob = fields.Date('Date of Birth')