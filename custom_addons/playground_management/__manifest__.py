# -*- coding: utf-8 -*-
{
    'name': "Playground",
    'summary': """""",
    'description': """""",
    'author': "",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'contacts'],

    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/playground_craft_view.xml',
        'views/res_partner_view.xml',
        'reports/playground_report.xml'

    ],

    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,

    'assets': {
        'web.assets_backend': ['/playground_management/static/src/css/playground.css'],
    }}
