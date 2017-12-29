{
    'name': 'Redmine Stat',
    'summary': """This module will add a record to store student details""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to store student details""",
    'author': 'Oleg Karpov',
    'company': 'Syntech',
    'website': 'http://www.syntech.com',
    'category': 'Tools',
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [
        'views/views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    "external_dependencies": {
        'python': ['python-redmine']
    },
}
