from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0') ## Disable closing app on escape
Config.set('graphics', 'window_state', 'maximized') ## Set screen to Maximized
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') ## Turns off red circles on left click

from pathlib import Path
import sqlite3

from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.uix.navigationdrawer import NavigationLayout
from kivymd.app import MDApp
from kivy.clock import Clock

import kivy.properties as prop

from lib.py.data_management import DataManagement
from lib.py.export_data import ExportData
from lib.py.pcd_tree import PCDTree
import lib.data_cls

def set_path(directory=''):
    """Sets path to current folder, if directory specified, creates folder inside working directory
    :param directory: str
    :return: str"""
    path = Path(f"./{directory}")
    if directory != '':
        path.mkdir(parents=True, exist_ok=True)
    return str(path.resolve()) + '/'

class MainFrame(NavigationLayout):
    """Main Frame of the application"""

    app = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ## Set up var to interact with main application \/
        self.app = MDApp.get_running_app()
        ## Add standard widgets to main frame \/
        self.ids.tree_frame.add_widget(self.app.pcd_tree)
        self.ids.export_frame.add_widget(self.app.export_data)

    def switch_to_screen(self,screen,duration=0.2):
        """Switch to screen
        :param screen: str
        :param duration: float
        """
        self.ids.screen_manager.current = screen

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

    ## Place holders for APP objects \/
    cursor = prop.ObjectProperty() ## Sqlite cursor
    pcd_tree = prop.ObjectProperty() ## PCD TreeView + widgets object
    main_frame = prop.ObjectProperty()  ## Main Frame object
    connection = prop.ObjectProperty() ## Sqlite connection
    export_data = prop.ObjectProperty() ## Export TreeView + widgets object
    data_management = prop.ObjectProperty() ## Data Management object, *text fields*

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ## Sets app themming \/
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Gray"
        ## Sets Sqlite connection and cursor \/
        self.connection = sqlite3.connect(f'{set_path("data")}database.db')
        self.cursor = self.connection.cursor()
        ## Sets up table PCD in sqlite \/
        lib.data_cls.create_tables()
        ## Instantiation of TreeView objects \/
        self.pcd_tree = PCDTree()
        self.export_data = ExportData()

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
        Clock.schedule_once(dismiss_welcome,1.5) ## Switches after 1.5 seconds

    def on_stop(self):
        ## Close Sqlite connection \/
        self.connection.close()

    def build(self):
        """Main APP builder"""
        self.main_frame = MainFrame() ## Main Frame object
        return self.main_frame

if __name__ == "__main__":
    ElPCD().run()