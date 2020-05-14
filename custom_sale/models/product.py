from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    article_number = fields.Char("Article Number")
    list_price = fields.Float(
        'Price excl.', default=1.0,
        digits='Product Price',
        help="Price at which the product is sold to customers.",translate=True)


class ProductProduct(models.Model):
    _inherit = "product.product"

    lst_price = fields.Float(
        'Price excl.', compute='_compute_product_lst_price',
        digits='Product Price', inverse='_set_product_lst_price',
        help="The sale price is managed from the product template. Click on the 'Configure Variants' button to set the extra attribute prices.",translate=True)