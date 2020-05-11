##############################################################################

{
    'name': "Sale Customization",

    'summary': """
         Sales Customizations.""",

    'description': """
       Sales Customizations
    """,

    'author': "PPTS India Pvt Ltd",
    'website': "https://pptssolutions.com",
    'category': 'Base',
    'version': '0.1',
    'depends': ['base','sale','product','website_sale'],
    'data': [
        'views/sale_view.xml',
        'views/product_view.xml',
    ],
}
