from odoo import fields, models, api, _

class ProductProduct(models.Model):
    _inherit = "product.template"

    article_number = fields.Char("Article Number")