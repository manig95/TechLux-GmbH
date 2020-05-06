from odoo import models, fields, api, _
import base64
import re
from PyPDF2 import PdfFileMerger


class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_no = fields.Char("Delivery Note No.")
