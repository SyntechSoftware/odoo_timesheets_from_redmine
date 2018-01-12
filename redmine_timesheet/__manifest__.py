{
    'name': 'Redmine Timesheets',
    'summary': """This module will add a record to store student details""",
    'version': '11',
    'description': """This module will add a record to store student details""",
    'author': 'Oleg Karpov',
    'company': 'Syntech Software',
    'website': 'http://syntech.software/',
    'category': 'Tools',
    'depends': ['hr_timesheet'],
    'license': 'AGPL-3',
    'data': [
        'views/redmine_menu.xml',
        'cron/fetch_data.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    "external_dependencies": {
        'python3': ['redminelib', 'python-redmine'],
        'pip3': ['python-redmine'],
        #for odoo 10
        'pip': ['python-redmine'],
    },
}
