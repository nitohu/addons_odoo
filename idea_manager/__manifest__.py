{
    'name': 'Idea Manager',
    'version': '15.0.1.0.0',
    'summary': 'Idea Manager',
    'description': '''Idea Manager''',
    'category': '',
    'author': 'Niklas Tom Hucke',
    'website': 'http://www.nitohu.de/',
    'license': 'AGPL-3',
    'depends': [
        'project',
    ],
    'data': [
        "security/groups.xml",
        "security/ir.model.access.csv",

        "views/menu.xml",
        "views/idea_idea.xml",
        "views/idea_tags.xml",
        "views/idea_category.xml",
        "views/project_project.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
