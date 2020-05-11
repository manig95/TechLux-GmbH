# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Inventory Customization',
    'version' : '13.0',
    'category': 'Website',
    'author': 'PPTS [India] Pvt.Ltd.',
    'website': 'www.pptssolutions.com',
    'description': """
Inventory Customization
==================
        """,
    'depends' : ['stock'],
    'data': [
        'views/stock_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
