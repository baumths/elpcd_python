from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0') ## Disable closing app on escape
Config.set('graphics', 'window_state', 'maximized') ## Set screen to Maximized
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') ## Turns off red circles on left click

from pathlib import Path
import sqlite3, sys, os
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock

import kivy.properties as prop

from lib.py.data_management import DataManagement
from lib.csv_export import ExportCSV
from lib.py.pcd_tree import PCDTree
import lib.data_cls

def set_path(directory=''):
    """Sets path to current folder, if directory specified, creates folder inside working directory
    :param directory: str
    :return: str"""
    path = Path(f".{os.sep}{directory}")
    if directory != '':
        path.mkdir(parents=True, exist_ok=True)
    return str(path.resolve())

class MainFrame(MDBoxLayout):
    """Main Frame of the application"""

    app = None
    export_dialog = prop.ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ## Set up var to interact with main application \/
        self.app = MDApp.get_running_app()
        ## Add standard widgets to main frame \/
        self.ids.tree_frame.add_widget(self.app.pcd_tree)

    def switch_to_screen(self,screen,duration=0.2):
        """Switch to screen
        :param screen: str
        :param duration: float
        """
        self.ids.screen_manager.current = screen
    
    def _export_csv(self, *args):
        """Callback for export dialog popup button"""
        try:
            ## try exporting data into .csv file
            self.export.export_data()
        except lib.utils.NotAbleToWriteFile:
            toast('Não foi possível criar o arquivo!')
        else:
            ## shows snackbar with path to new .csv file
            self.export_dialog.dismiss()
            snackbar = Snackbar(text=f'PCD exportado para {self.export.new_file}',duration=10)
            snackbar.show()

    def confirm_export_dialog(self):
        """Create and open export dialog popup"""
        btn_cancel = MDFlatButton(text='Cancelar',theme_text_color='Custom',text_color= self.app.theme_cls.primary_dark)
        btn_confirm = MDRaisedButton(text= 'Exportar .CSV',elevation= 11,on_release= self._export_csv)
        self.export_dialog = MDDialog(
            title= 'Deseja exportar seu PCD?',
            text= f'Salvando em {self.export.get_path()}',
            auto_dismiss= False,
            buttons= [btn_cancel,btn_confirm])
        self.export_dialog.buttons[0].bind(on_release= self.export_dialog.dismiss)
        self.export_dialog.open()
    
    def open_export_dialog(self, *args):
        """Callback for Export button"""
        self.export = ExportCSV(name='PCD') ## Prepares for file export 
        self.confirm_export_dialog() ## Opens dialog

class Manager(ScreenManager):
    """Screen Manager Class"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ## Sets transition of Screen Manager \/
        self.transition = FadeTransition()

class ElPCD(MDApp):
    """Main App Class"""

    ## Repository name, user will be able to change in the future \/
    REPOSITORY = prop.StringProperty('ElPCD')
    LOGO = prop.StringProperty()

    ## Place holders for APP objects \/
    cursor = prop.ObjectProperty() ## Sqlite cursor
    pcd_tree = prop.ObjectProperty() ## PCD TreeView + widgets object
    main_frame = prop.ObjectProperty()  ## Main Frame object
    connection = prop.ObjectProperty() ## Sqlite connection
    data_management = prop.ObjectProperty() ## Data Management object, *text fields*

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ## Load logo image \/
        self.LOGO = os.path.join(os.environ["ELPCD_ROOT"],'assets','gedalogo2020.png')
        ## Sets app themming \/
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Gray"
        ## Sets Sqlite connection and cursor \/
        self.connection = sqlite3.connect(os.path.join(set_path("data"),'database.db'))
        self.cursor = self.connection.cursor()
        ## Sets up table PCD in sqlite \/
        lib.data_cls.create_tables()
        ## Instantiation of TreeView objects \/
        self.pcd_tree = PCDTree()

    def set_data_management_widget(self, view_only=True,item_data=None,new_cls=False):
        """Clear and add new Data Management object,
        view_only locks the text fields,
        item_data contains from the database,
        new_cls creates an item without any parents. 
        :param view_only: bool
        :param item_data: dict
        :param new_cls: bool
        """
        self.main_frame.ids.data_frame.clear_widgets()
        self.data_management = DataManagement(view_only=view_only,item_data=item_data,new_cls=new_cls)
        self.main_frame.ids.data_frame.add_widget(self.data_management)

    def on_start(self):
        def dismiss_welcome(*args):
            """Switch off of welcome screen"""
            self.main_frame.switch_to_screen('pcd',duration=5.)
        self.welcome_event = Clock.schedule_once(dismiss_welcome,5) ## Switches after 5 seconds

    def on_stop(self):
        ## Close Sqlite connection \/
        self.connection.close()

    def build(self):
        """Main APP builder"""
        self.main_frame = MainFrame() ## Main Frame object
        return self.main_frame

if __name__ == "__main__":

    if hasattr(sys, "_MEIPASS"):
        from kivy.resources import resource_add_path
        os.environ["ELPCD_ROOT"] = sys._MEIPASS
        resource_add_path(os.environ["ELPCD_ROOT"])

        Builder.load_file(os.path.join(os.environ["ELPCD_ROOT"],'elpcd.kv'))
    else:
        os.environ["ELPCD_ROOT"] = os.path.dirname(os.path.abspath(__file__))

    kv_files_dir = os.path.join(os.environ["ELPCD_ROOT"],'lib','kv')
    for item in os.listdir(kv_files_dir):
        Builder.load_file(os.path.join(kv_files_dir, item))

    ElPCD().run()