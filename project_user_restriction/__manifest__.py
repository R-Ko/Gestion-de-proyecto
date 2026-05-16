{
    'name': 'Project: Restrict visibility to assigned users',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Restrict project visibility so users only see projects assigned to them',
    'depends': ['project'],
    'data': [
        'security/project_user_restriction_security.xml',
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/wizard_change_password.xml',
    ],
    'installable': True,
    'application': False,
}
