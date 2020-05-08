from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'resizable', 0)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

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
    path = Path(f"./{directory}")
    if directory != '':
        path.mkdir(parents=True, exist_ok=True)
    return str(path.resolve()) + '/'

class MainFrame(NavigationLayout):

    app = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

        self.ids.tree_frame.add_widget(self.app.pcd_tree)
        self.ids.export_frame.add_widget(self.app.export_data)

    def switch_to_screen(self,screen,duration=0.2):
        self.ids.screen_manager.current = screen

class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()

class ElPCD(MDApp):

    tv = prop.ObjectProperty()
    cursor = prop.ObjectProperty()
    main_frame = prop.ObjectProperty()
    connection = prop.ObjectProperty()
    export_data = prop.ObjectProperty()
    drawer_content = prop.ObjectProperty()
    data_management = prop.ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Gray"

        self.connection = sqlite3.connect(f'{set_path("data")}database.db')
        self.cursor = self.connection.cursor()

        lib.data_cls.create_table('PCD')

        self.pcd_tree = PCDTree()
        self.export_data = ExportData()

    def set_data_management_widget(self, view_only=True,item_data=None,new_cls=False):
        self.main_frame.ids.data_frame.clear_widgets()
        self.data_management = DataManagement(view_only=view_only,item_data=item_data,new_cls=new_cls)
        self.main_frame.ids.data_frame.add_widget(self.data_management)

    def on_start(self):
        def dismiss_welcome(*args):
            self.main_frame.switch_to_screen('pcd',duration=5.)
        Clock.schedule_once(dismiss_welcome,1.5)

    def on_stop(self):
        self.connection.close()

    def build(self):
        self.main_frame = MainFrame()
        return self.main_frame

if __name__ == "__main__":
    ElPCD().run()