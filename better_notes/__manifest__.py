{
    'name': 'Better Notes',
    'version': '15.0.0.0.1',
    'summary': 'Better Notes - share notes with others, secure them with password and delete them after some time.',
    'description': '''
Better Notes
============

Share notes with others, secure them with password and delete them after some time.
    ''',
    'category': 'Notes',
    'author': 'Niklas Tom Hucke',
    'website': 'http://www.nitohu.de/',
    'license': 'AGPL-3',
    'depends': [
        'note',
        'web'
    ],
    'data': [
        "views/note_note.xml",

        "views/note_templates.xml"
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
