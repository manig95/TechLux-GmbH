from odoo import models, fields, api, _
import base64
import re
from PyPDF2 import PdfFileMerger


class AccountMove(models.Model):
    _inherit = 'account.move'

    pdf_file = fields.Binary("PDF File")
    pdf_name = fields.Char("PDF Name")
    pdf_2 = fields.Binary("PDF 2")
    pdf_2name = fields.Char("Pdf 2 name")

    def print_esr_report(self):
        invoice_report = self.env['ir.actions.report']._get_report_from_name("account.report_invoice")
        inv_pdf_report = invoice_report.render_qweb_pdf(self.id)[0]
        inv_rp = base64.b64encode(inv_pdf_report)

        esr_report = self.env.ref('l10n_ch.l10n_ch_isr_report').render_qweb_pdf(self.id)[0]
        esr_pdf = base64.b64encode(esr_report)

        self.pdf_file = inv_rp
        self.pdf_name = self.name + "_Invoice.pdf"

        self.pdf_2 = esr_pdf
        self.pdf_2name = self.name + "_ESR.pdf"

        pdfs = [self.pdf_file, self.pdf_2]

        merger = PdfFileMerger()

        for pdf in pdfs:
            merger.append(pdf, import_bookmarks=False)

        self.pdf_file = merger.write(str(self.name + "_Invoice_esr.pdf"))
        merger.close()


        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=account.move&id={}&field=pdf_file&filename_field=pdf_name&download=true'.format(self.id),
            'target': 'self',
        }