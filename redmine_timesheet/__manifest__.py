{
    'name': 'Redmine Timesheets',
    'summary': """This module will allow to populate data from redmine to odoo existing modules""",
    'version': '1.0',
    'description': """This module will allow to populate data from redmine to odoo existing modules""",
    'author': 'Oleg Karpov',
    'company': 'Syntech Software',
    'website': 'http://syntech.software/',
    'category': 'Extra Tools',
    'depends': ['hr_timesheet'],
    'license': 'AGPL-3',
    'data': [
        'views/redmine_timesheet_menu_item.xml',
        'views/res_config_settings_views.xml',
        'cron/fetch_data.xml',
    ],
    'demo': [
        # 'demo/demo.xml'
    ],
    "external_dependencies": {
        'python': ['redminelib'],
    },
    'installable': True,
    'application': True,
}
