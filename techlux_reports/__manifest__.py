# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'TechLux Report Customization',
    'version': '1',
    'category': 'Sale,account',
    'author': 'PPTS India Pvt  Ltd',
    'summary': 'TechLux Report Customization',
    'description': """
                TechLux Report Customization
                    """,
    'depends': ['web', 'sale', 'stock', 'delivery', 'account'],
    'data': [
        "views/invoice_view.xml",
        "report/report_layout.xml",
        "report/sale_report_template.xml",
        "report/picking_report.xml",
        "report/invoice_report.xml",
        "report/invoice_with_esr.xml",
        "report/delivery_slip.xml",
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
