# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'COD Payment',
    'version' : '13.0',
    'category': 'Website',
    'summary': 'COD Payment',
    'author': 'PPTS [India] Pvt.Ltd.',
    'website': 'www.pptssolutions.com',
    'description': """
Odoo E-Commerce
==================
        """,
    'depends' : ['payment', 'web', 'website', 'website_sale'],
    'data': [
        'views/payment_acquirer.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
