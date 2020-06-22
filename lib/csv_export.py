from kivymd.app import MDApp

from datetime import datetime
import csv

import lib.gen_ref_code
import lib.utils
import lib.paths

class ExportCSV:
    """Export .csv object"""

    ## Place holders \/
    app = None ## Main APP reference
    name = None ## name for file
    path_to_file = None ## file path + name
    exports_directory = None ## directory to export files

    def __init__(self, name='PCD'):
        self.app = MDApp.get_running_app() ## App object reference
        self.name = name
        self.exports_directory = self.create_path()

    def export_data(self):
        """Exports data to .csv file"""
        description,table = self.fetch_data() ## get data from database
        table = self._add_ref_code(table) ## adds reference codes for each row
        repository = self.create_repository_row() ## create repo tupple
        try:
            self.path_to_file = self.gen_path_to_file() ## returns file path 
            ## tries to write data to file \/
            with open(self.path_to_file, 'w') as file:
                write = csv.writer(file, lineterminator='\n')
                write.writerow(description) ## write headers
                write.writerow(repository) ## write repo line
                write.writerows(table) ## write all data
        except:
            raise lib.utils.NotAbleToWriteFile()


    def create_repository_row(self):
        """Create repo row, user will be able
        to change repo name in the future 
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
        """Fetches data from database to
        accesstomemory.org importing standards 
        returns a tupple of `(description,table)`
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

    def _add_ref_code(self, table):
        """Generates reference codes
        for each row in database table 
        :param table: list
        :return: list"""
        ref_codes = lib.gen_ref_code.generate_reference_codes()
        for item in table:
            for code in ref_codes:
                if item[1] == code['legacyId']:
                    item[0] = code['codigo_ref']
                    ref_codes.remove(code)
        return table

    def get_datetime(self):
        """Returns current date and time
        :return: str"""
        return datetime.now().strftime('%d-%m-%Y_%Hh%Mmin%Ss')
    
    def create_path(self):
        """Creates the exports directory
        and returns a path object
        :return: obj"""
        dir_path = lib.paths.CWD / 'ElPCD_Exports' ## creates path object
        dir_path.mkdir(parents=True, exist_ok=True) ## creates folder if not exists
        return dir_path
    
    def gen_path_to_file(self):
        """Creates the name and returns
        the full path to a new file
        :return: str"""
        file_name = f'{self.name}_{self.get_datetime()}.csv' ## creates file name
        full_path = self.exports_directory / file_name ## joins path and file name togheter
        return str(full_path.resolve())
    
    def get_path(self):
        """Returns path to exports folder
        :return: str"""
        return str(self.exports_directory.resolve())