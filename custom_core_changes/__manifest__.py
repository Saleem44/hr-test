# -*- encoding: utf-8 -*-
##############################################################################

##############################################################################
{
    'name': 'Custom Core Changes',
    'summary': 'Custom Core Changes',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': """
Custom Core Changes
""",
    'author': "ALI",
    'website': 'https://www.example.com/',
    'depends': ['base', 'web', 'hr', 'hr_skills', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_core_menu.xml',
        'views/custom_core_views.xml',
        'wizard/project_wiz_view.xml',
        'data/ir_cron_data.xml',
    ],
    "assets": {
        "web.assets_backend": [
             'custom_core_changes/static/src/js/custom_usermenu.js',
             'custom_core_changes/static/src/js/custom_user_menu_items.js',
             'custom_core_changes/static/src/css/custom_css.css',
        ],

    },
    'installable': True,
    'application': True,
}
