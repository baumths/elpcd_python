from kivymd.app import MDApp

from datetime import datetime
from pathlib import Path
import csv
import os

import lib.gen_ref_code
import lib.utils

class ExportCSV:
    """Export .csv object"""

    ## Place holders \/
    app = None ## Main APP reference
    name = None ## name for file
    new_file = None ## file path + name
    _datetime = None ## time and date
    _file_name = None ## name of the file
    _file_path = None ## path to file

    def __init__(self, name='PCD'):
        self.app = MDApp.get_running_app() ## App object reference
        self.name = name
        self._file_path = self.set_path('ElPCD_Exports') ## create exports directory

    def export_data(self):
        """Exports data to .csv file"""
        description,table = self.fetch_data() ## get data from database
        table = self._add_ref_code(table) ## adds reference codes for each row
        repository = self.create_repository_row() ## create repo tupple
        try:
            ## tries to write data to file 
            self.set_file_name()
            self.new_file = self.get_path()+self.get_file_name() ## sets file path + name 
            with open(self.new_file, 'w') as file:
                write = csv.writer(file, lineterminator='\n')
                write.writerow(description) ## write headers
                write.writerow(repository) ## write repo line
                write.writerows(table) ## write all data
        except:
            raise lib.utils.NotAbleToWriteFile()

    def get_datetime(self):
        """Get current date and time"""
        return datetime.now().strftime('%d-%m-%Y_%H:%M:%S')

    def create_repository_row(self):
        """Create repo row, user will be to change repo name in the future 
        :return: tupple"""
        ## Repo constant in main app object \/
        repo = (
            self.app.REPOSITORY,
            'zero',
            '',
            self.app.REPOSITORY,
            self.app.REPOSITORY,
            '',
            '',
            self.app.REPOSITORY)
        return repo

    def fetch_data(self):
        """Fetches data from database to accesstomemory.org importing standards 
        returns tupple of (description,table) lists
        :return: tupple"""
        self.app.cursor.execute('''
        SELECT '' as referenceCode, legacyId, parentId,
        cls_codigo as identifier, cls_nome as title,

        'Registro de abertura: '||reg_abertura||'\n'||
        'Registro de desativação: '||reg_desativacao||'\n'||
        'Indicador de classe ativa/inativa: '||cls_indicador as scopeAndContent,

        'Reativação de classe: '||reg_reativacao||'\n'||
        'Registro de mudança de nome de classe: '||reg_mudanca_nome||'\n'||
        'Registro de deslocamento de classe: '||reg_deslocamento ||'\n'|| 
        'Registro de extinção: '||reg_extincao as arrangement,
        '' as repository,

        'Prazo de guarda na fase corrente: '||fase_corrente||'\n'||
        'Evento que determina a contagem do prazo de guarda na fase corrente: '||evento_fase_corrente||'\n'||
        'Prazo de guarda na fase intermediária: '||fase_intermediaria||'\n'||
        'Evento que determina a contagem do prazo de guarda na fase intermediária: '||evento_fase_inter||'\n'||
        'Destinação final: '||dest_final||'\n'||
        'Registro de alteração: '||reg_alteracao||'\n'||
        'Observações: '||observacoes as appraisal

        FROM PCD''')

        table = [ list(item) for item in self.app.cursor.fetchall() ]
        description = [ col[0] for col in self.app.cursor.description]
        return description,table

    def _add_ref_code(self,table):
        """Generates reference codes for each row in database table 
        :param table: list
        :return: list"""
        ref_codes = lib.gen_ref_code.generate_reference_codes()
        for item in table:
            for code in ref_codes:
                if item[1] == code['legacyId']:
                    item[0] = code['codigo_ref']
                    ref_codes.remove(code)
        return table

    def set_path(self, directory):
        """Creates folder inside working directory and set path to current folder
        :param directory: str
        :return: str"""
        path = Path(f'.{os.sep}{directory}')
        path.mkdir(parents=True, exist_ok=True)
        return str(path.resolve()) + os.sep
    
    def get_path(self):
        """File path getter
        :return: str"""
        return str(self._file_path)
    
    def set_file_name(self):
        """File name setter"""
        self._file_name = f'{self.name}_{self.get_datetime()}.csv'
    
    def get_file_name(self):
        """File name getter"""
        return str(self._file_name)