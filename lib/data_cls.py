from kivymd.app import MDApp

class ManageData:
    item_data = None
    parent_id = None
    def __init__(self,item_data={},parent_id=''):
        """
        :param item_data: dict
        :param parent_id: str
        """
        self.app = MDApp.get_running_app()
        self.item_data = item_data
        self.parent_id = parent_id
    
    def insert_into_db(self):
        """
        Inserts into database
        """
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
            cls_indicador) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        values = (self.parent_id, *[ item for x,item in self.item_data.items() if x not in ('legacyId','parentId') ])
        self.app.cursor.execute(sql, values)
        self.app.connection.commit()

    def update_db(self):
        """
        Updates database
        """
        sql = '''UPDATE PCD SET 
            cls_nome == ?,
            cls_codigo == ?,
            reg_abertura == ?,
            reg_desativacao == ?,
            reg_reativacao == ?,
            reg_mudanca_nome == ?,
            reg_deslocamento == ?,
            reg_extincao == ?,
            cls_indicador == ?
            WHERE legacyId == ?'''
        valores = (
            self.item_data['cls_nome'],
            self.item_data['cls_codigo'],
            self.item_data['reg_abertura'],
            self.item_data['reg_desativacao'],
            self.item_data['reg_reativacao'],
            self.item_data['reg_mudanca_nome'],
            self.item_data['reg_deslocamento'],
            self.item_data['reg_extincao'],
            self.item_data['cls_indicador'],
            self.parent_id
        )
        self.app.cursor.execute(sql, valores)
        self.app.connection.commit()





def create_table(table=''):
    app = MDApp.get_running_app()
    if table == 'PCD':
        app.cursor.execute('''
        CREATE TABLE IF NOT EXISTS PCD (
        legacyId INTEGER PRIMARY KEY AUTOINCREMENT,
        parentId INTEGER,
        cls_nome TEXT NOT NULL,
        cls_codigo varchar(20) NOT NULL,
        cls_sub varchar(20),
        reg_abertura TEXT,
        reg_desativacao TEXT,
        reg_reativacao TEXT,
        reg_mudanca_nome TEXT,
        reg_deslocamento TEXT,
        reg_extincao TEXT,
        cls_indicador VARCHAR(7)
        )''')
    elif table == 'TTD':
        pass
        """
        app.cursor.execute('''
        CREATE TABLE IF NOT EXISTS TTD (
        cls_codigo varchar(20) NOT NULL,
        prazo_guarda_fase_corrente INT(20),
        evento_determina_prazo_fase_corrente TEXT,
        prazo_guarda_fase_intermediaria INT(20),
        evento_contagem_prazo_guarda_fase_intermediaria TEXT,
        dest_final varchar(20),
        reg_alteracao TEXT,
        Observacoes TEXT,
        FOREIGN KEY (cls_codigo) references PCD(cls_codigo),
        );''')
        """
    else:
        print(f"[\033[1;31mERROR  \033[m] Couldn't create table {table}!")
    app.connection.commit()

def delete_row(item_data):
    app = MDApp.get_running_app()
    children = app.cursor.execute('SELECT * FROM PCD WHERE parentId == ?',(item_data['legacyId'],)).fetchall()
    if children:
        raise Exception('Classe possui dependentes!')
    else:
        app.cursor.execute('DELETE FROM PCD WHERE legacyId == ?',(item_data['legacyId'],))
        app.connection.commit()
    
def drop_table(table):
    app = MDApp.get_running_app()
    try:
        app.cursor.execute(f'DELETE FROM {table}')
        app.connection.commit()
    except:
        raise Exception('Impossível apagar dados!')
    else:
        create_table(table)
