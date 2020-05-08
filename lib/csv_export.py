from kivymd.app import MDApp

from datetime import datetime
from pathlib import Path
import csv

class ExportCSV():
    
    _file_path = None
    _file_name = None
    _datetime = None
    new_file = None
    name = None
    app = None

    def __init__(self, name='PCD'):
        self.app = MDApp.get_running_app()
        self.name = name
        self._file_path = self.set_path('ElPCD_Exports')

    def export_data(self):
        description,table = self.fetch_data()
        repository = self.create_repository()
        try:
            self.set_file_name()
            self.new_file = self.get_path()+self.get_file_name()
            with open(self.new_file, 'w') as file:
                write = csv.writer(file, lineterminator='\n')
                write.writerow(description)
                write.writerow(repository)
                write.writerows(table)
        except:
            raise Exception('Não foi possível criar o arquivo!')

    def get_datetime(self):
        return datetime.now().strftime('%d-%m-%Y_%H:%M:%S')

    def create_repository(self):
        repo = 'PCD'
        return ('zero','',repo,repo,'','',repo)

    def fetch_data(self):
        self.app.cursor.execute('''
        SELECT legacyId, parentId, cls_codigo as identifier, cls_nome as title,

        'Registro de Abertura: ' || reg_abertura || '\n' ||
        'Registro de Desativação: ' || reg_desativacao || '\n' ||
        'Indicador de Classe Ativa/Inativa: ' || cls_indicador as scopeAndContent,

        'Reativação de Classe: ' || reg_reativacao || '\n' ||
        'Registro de Mudança de Nome de Classe: ' || reg_mudanca_nome || '\n' ||
        'Registro de Deslocamento de Classe: ' || reg_deslocamento || '\n' || 
        'Registro de Extinção: ' || reg_extincao as arrangement,
        '' as repository

        FROM PCD''')

        table = self.app.cursor.fetchall()
        description = [ col[0] for col in self.app.cursor.description]
        return description,table

    def set_path(self, directory):
        path = Path(f'./{directory}')
        path.mkdir(parents=True, exist_ok=True)
        return str(path.resolve()) + '/'
    
    def get_path(self):
        return str(self._file_path)
    
    def set_file_name(self):
        self._file_name = f'{self.name}_{self.get_datetime()}.csv'
    
    def get_file_name(self):
        return str(self._file_name)