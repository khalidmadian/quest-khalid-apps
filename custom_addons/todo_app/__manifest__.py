# -*- coding: utf-8 -*-
{
    'name': "To-Do App",
    'summary': """""",
    'description': """""",
    'author': "",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml'
    ],

    'installable': True,
    'application': True,
}
