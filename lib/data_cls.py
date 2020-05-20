from kivymd.app import MDApp
import lib.utils

class ManageData:
    """Data manager for inserting and updating database rows"""

    item_data = None ## Dict of data to be inserted/updated
    parent_id = None ## Parent id for item_data
    parent_data = None ## Dict of parent data 

    def __init__(self,item_data,parent_data):
        """
        :param item_data: dict
        :param parent_id: str
        """
        self.app = MDApp.get_running_app() ## App object reference
        self.item_data = item_data
        self.parent_data = parent_data
        ## Sets parent id to zero if item is going to be a parent \/
        self.parent_id = 'zero' if parent_data == 'zero' else parent_data['legacyId']
    
    def insert_into_db(self):
        """Inserts item_data into database"""
        sql = '''INSERT INTO PCD (
            parentId,
            cls_nome,
            cls_codigo,
            cls_sub,
            reg_abertura,
            reg_desativacao,
            reg_reativacao,
            reg_mudanca_nome,
            reg_deslocamento,
            reg_extincao,
            cls_indicador,

            fase_corrente,
            evento_fase_corrente,
            fase_intermediaria,
            evento_fase_inter,
            dest_final,
            reg_alteracao,
            observacoes) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        exclude = ('legacyId','parentId','codigo_ref')
        items = [ item for x,item in self.item_data.items() if x not in exclude ]
        values = (self.parent_id, *items)
        self.app.cursor.execute(sql, values)
        self.app.connection.commit()

    def update_db(self):
        """Updates database row based on item_data"""
        sql = '''UPDATE PCD SET 
            cls_nome == ?,
            cls_codigo == ?,
            reg_abertura == ?,
            reg_desativacao == ?,
            reg_reativacao == ?,
            reg_mudanca_nome == ?,
            reg_deslocamento == ?,
            reg_extincao == ?,
            cls_indicador == ?,

            fase_corrente == ?,
            evento_fase_corrente == ?,
            fase_intermediaria == ?,
            evento_fase_inter == ?,
            dest_final == ?,
            reg_alteracao == ?,
            observacoes == ?
            WHERE legacyId == ?'''
        exclude = ('legacyId','parentId','cls_sub','codigo_ref')
        items = [ item for x,item in self.item_data.items() if x not in exclude]
        values = (*items,self.parent_id)
        self.app.cursor.execute(sql, values)
        self.app.connection.commit()


def create_tables():
    """Creates database tables, currently only 'PCD' table """
    app = MDApp.get_running_app() ## App object reference
    try:
        app.cursor.execute('''
        CREATE TABLE IF NOT EXISTS PCD (
        legacyId INTEGER PRIMARY KEY AUTOINCREMENT,
        parentId INTEGER,
        cls_nome TEXT NOT NULL,
        cls_codigo VARCHAR(20) NOT NULL,
        cls_sub VARCHAR(20),
        reg_abertura TEXT,
        reg_desativacao TEXT,
        reg_reativacao TEXT,
        reg_mudanca_nome TEXT,
        reg_deslocamento TEXT,
        reg_extincao TEXT,
        cls_indicador VARCHAR(20),

        fase_corrente TEXT,
        evento_fase_corrente TEXT,
        fase_intermediaria TEXT,
        evento_fase_inter TEXT,
        dest_final VARCHAR(20),
        reg_alteracao TEXT,
        observacoes TEXT
        )''')
    except:
        print(f"[\033[1;31mERROR  \033[m] Couldn't create table!")
    else:
        app.connection.commit()

def delete_row(item_data):
    """Delete row from database if item has no children"""
    app = MDApp.get_running_app() ## App object reference
    children = app.cursor.execute('SELECT * FROM PCD WHERE parentId == ? LIMIT 1',(item_data['legacyId'],)).fetchone()
    if children:
        raise lib.utils.ItemHasChildren()
    else:
        app.cursor.execute('DELETE FROM PCD WHERE legacyId == ?',(item_data['legacyId'],))
        app.connection.commit()
    
def drop_table():
    """Delete the entire 'PCD' table and regenerates table"""
    app = MDApp.get_running_app() ## App object reference
    try:
        app.cursor.execute(f'DELETE FROM PCD')
        app.connection.commit()
    except:
        raise lib.utils.NotAbleToDeleteDB()
    else:
        create_tables()