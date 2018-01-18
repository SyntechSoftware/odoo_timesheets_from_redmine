Odoo Redmine Timesheets
---------------
The app allows transferring and synchronization objects from Redmine (project, issue, time entry) to Odoo (project,
task, employee, timesheet). The synchronization is set up by cron tasks.

A Simple User Interface
----------------------
1. Install app Redmine Timesheet.
2. Go to Settings --> General Settings --> Redmine Credentials
    - Set Redmine API Key
    - Set Redmine URL

3. Click Save and projects, tasks, timesheets, employees will be populated in odoo.
4. Also cron task will be activated, and once in a day new data from redmine will be synced and populated in odoo.
