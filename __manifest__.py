# -*- coding: utf-8 -*-
{
    'name': "training odoo",

    'summary': """
        Training Odoo from tutorial open erp""",

    'description': """
        Training Odoo from tutorial open erp
    """,

    'author': "Galang AS",
    'website': "#",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/scheduler_data.xml',
        'views/sequence.xml',
        'views/views.xml',
        'views/partner.xml',
        'views/course.xml',
        'views/session.xml',
        'views/attendee.xml',
        'wizard/training_wizard_views.xml',
        'views/templates.xml',
        # 'demo/demo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
