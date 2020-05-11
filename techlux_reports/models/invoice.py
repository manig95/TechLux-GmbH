from odoo import models, fields, api, _
import base64
import re
from PyPDF2 import PdfFileMerger


class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_no = fields.Char("Delivery Note No.")

    def print_invoice(self):
        self.ensure_one()
        return self.env.ref('techlux_reports.l10n_ch_isr_report_with_invoice').report_action(self)
