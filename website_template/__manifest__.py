{
    # Theme information

    'name': 'Website Customization',
    'category': 'Web Theme',
    'summary': 'Fully Responsive Odoo Theme suitable for eCommerce Businesses',
    'depends': [
       'website','theme_clarico','website_form','website_sale','product','emipro_theme_base',
    ],

    'data': [
        'views/home_page_template.xml',
        # 'views/allgemeine_page_template.xml',
        # 'views/bestellung_page_template.xml',
        # 'views/faq_page_template.xml',
        # 'views/versand_page_template.xml',
        'views/imperssum_page_template.xml',
        'views/datenschutz_template.xml',
        'views/aboutus_template.xml',
        'views/shop_page_template.xml',
    ],

    'author': 'PPTS India Pvt. Ltd.',
    'website': 'https://www.pptssolutions.com',
    # Technical
    'installable': True,
    'auto_install': False,
}
