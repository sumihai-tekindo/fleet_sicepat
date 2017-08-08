{
    'name': 'Fleet Edit',
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Generic Modules/Fleet Edit',
    'author': 'Andrean Wijaya',
    'website': '-',
    'depends': ['account','fleet','account_asset'],
    'data': [
        'views/fleet_service_type.xml',
        'views/fleet_edit_view.xml',
        'views/fleet_tools_view.xml',
        'views/template_email_fleet.xml',
        'views/fleet_status.xml',
        'views/cron_fleet.xml',
    ],
    'installable': True,
}
