from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.app import MDApp

import kivy.properties as prop

from lib.py.data_tree import DataTree
from lib.csv_export import ExportCSV
import lib.utils

Builder.load_file('./lib/kv/export_data.kv')

class ExportData(MDBoxLayout):
    """Export screen widgets object"""

    ## Place holders \/
    app = None ## Main APP reference
    export = prop.ObjectProperty() ## obj for exporting data
    data_tree = prop.ObjectProperty() ## treeview object
    export_dialog = prop.ObjectProperty() ## export dialog popup
    btn_icon = prop.ListProperty(['unfold-more-horizontal','unfold-less-horizontal'])
    btn_text = prop.ListProperty(['Expandir Árvore', 'Retrair Árvore'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app() ## App object reference
        self.export = ExportCSV(name='PCD') ## Exporting .csv object

        self.data_tree = DataTree(view_only=True) ## treeview object
        self.ids.tree_frame.add_widget(self.data_tree) ## add treeview to screen

    def export_csv(self):
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
        btn_cancel = MDFlatButton(
            text= 'Cancelar',
            theme_text_color= 'Custom',
            text_color= self.app.theme_cls.primary_dark,
            on_release= lambda x: self.export_dialog.dismiss())
        btn_confirm = MDRaisedButton(
            text= 'Exportar .CSV',
            elevation= 11,
            on_release= lambda *x: self.export_csv())

        self.export_dialog = MDDialog(
            title= 'Deseja exportar seu PCD?',
            text= f'Salvando em {self.export.get_path()}',
            buttons= [btn_cancel,btn_confirm],
            auto_dismiss= False)
        self.export_dialog.open()
    
    def switch_button(self,reset=False):
        """Switches tooltip and icon when pressed"""
        if reset:
            self.btn_icon = ['unfold-more-horizontal','unfold-less-horizontal']
            self.btn_text = ['Expandir Árvore', 'Retrair Árvore']
        else:
            self.btn_icon[0], self.btn_icon[1] = self.btn_icon[1], self.btn_icon[0]
            self.btn_text[0], self.btn_text[1] = self.btn_text[1], self.btn_text[0]