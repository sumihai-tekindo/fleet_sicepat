{
    'name': 'Fleet Contract (when expired, automatically appear in supplier invoice)',
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Fleet Contract',
    'author': 'Aditya Nugraha',
    'website': '-',
    'depends': ['account','fleet','account_asset','base'],


     'data': [
        'views/fleet_contract_view.xml',
    ],


    'installable': True,
}
