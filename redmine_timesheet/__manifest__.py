{
    'name': 'Redmine Timesheets',
    'summary': """This module will add a record to store student details""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to store student details""",
    'author': 'Oleg Karpov',
    'company': 'Syntech',
    'website': 'http://www.syntech.com',
    'category': 'Tools',
    'depends': ['web', 'hr_timesheet'],
    'license': 'AGPL-3',
    'data': [
        'views/redmine_menu.xml',
        'views/tree_view_asset.xml'
        # 'views/redmine_backend_view.xml',
    ],
    'qweb': ['static/src/xml/tree_view_button.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    "external_dependencies": {
        'python3': ['redminelib', 'python-redmine'],
        'pip3': ['python-redmine']
    },
}
