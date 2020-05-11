
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_round, float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    line_number = fields.Integer("Pos.",default=1)
    product_code = fields.Char("Article Number/EAN Code")


    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        res = super(StockMove, self)._prepare_move_line_vals(self, quantity=None, reserved_quant=None)
        if self.sale_line_id:
            res.update({'product_code': self.env["sale.order.line"].browse(self.sale_line_id).product_code})
        return res