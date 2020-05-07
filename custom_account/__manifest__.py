# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Account Customization',
    'version' : '13.0',
    'category': 'Website',
    'summary': 'COD Payment',
    'author': 'PPTS [India] Pvt.Ltd.',
    'website': 'www.pptssolutions.com',
    'description': """
Account Customization
==================
        """,
    'depends' : ['account'],
    'data': [
        'views/account_move.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
