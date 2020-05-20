from kivymd.app import MDApp
"""
This file has functions to generate reference codes for each row in database table 'PCD' 
"""
def _fetch_db_into_dict():
    """Fetch entire database table into dictionary"""
    app = MDApp.get_running_app()
    table = app.cursor.execute('SELECT * FROM PCD').fetchall()
    description = [ col[0] for col in app.cursor.description ]
    return [ dict(zip(description,item)) for item in table ]

def _fetch_item_from_db(code):
    """Fetches data from database based on code = 'legacyId' 
    :param code: str
    :return: dict"""
    app = MDApp.get_running_app() ## App object reference
    app.cursor.execute(f'SELECT  * FROM PCD WHERE legacyId == {code}')
    item = app.cursor.fetchone()
    description = [ col[0] for col in app.cursor.description ]
    return dict(zip(description,item))

def _build_reference_code(child):
    """Recursive function to build reference code 
    :param child: str"""
    app = MDApp.get_running_app() ## App object reference
    if child['parentId'] == 'zero': ## base case, child has no parent
        return f'{app.REPOSITORY} {child["cls_codigo"]}'
    else:
        parent = _fetch_item_from_db(child['parentId'])
        return f"{_build_reference_code(parent)}-{child['cls_codigo']}"

def generate_reference_codes():
    """Generates reference codes for all rows in table 
    :return: list"""
    table = _fetch_db_into_dict()
    for row in table:
        row['codigo_ref'] = _build_reference_code(row)
    return table