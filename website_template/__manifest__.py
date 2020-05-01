{
    # Theme information

    'name': 'Website Customization',
    'category': 'Web Theme',
    'summary': 'Fully Responsive Odoo Theme suitable for eCommerce Businesses',
    'depends': [
      'website','emipro_theme_base','website_form','website_sale','product',
    ],

    'data': [
        'views/home_page_template.xml',
        'views/imperssum_page_template.xml',
        'views/datenschutz_template.xml',
        'views/aboutus_template.xml',
        'views/shop_page_template.xml',
        'views/signup_form.xml',
        'views/checkout_form.xml'
    ],

    'author': 'PPTS India Pvt. Ltd.',
    'website': 'https://www.pptssolutions.com',
    # Technical
    'installable': True,
    'auto_install': False,
}
