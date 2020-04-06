{
    "name": "Send Preview mail",
    "summary": "Send Preview mail",
    "version": "12.0",
    "category": "Social Network",
    "website": "http://pptssolutions.com",
    "author": "PPTS India Ltd",
    "license": "AGPL-3",
    "application": True,
    'installable': True,
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "wizard/send_preview_mail_wizard.xml",
        "views/send_mail_preview_mail.xml",
    ],
}
