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

Builder.load_file('./lib/kv/export_data.kv')

class ExportData(MDBoxLayout):

    app = None
    export = prop.ObjectProperty()
    data_tree = prop.ObjectProperty()
    export_dialog = prop.ObjectProperty()
    btn_icon = prop.ListProperty(['unfold-more-horizontal','unfold-less-horizontal'])
    btn_text = prop.ListProperty(['Expandir Árvore', 'Retrair Árvore'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.export = ExportCSV(name='PCD')

        self.data_tree = DataTree(view_only=True)
        self.ids.tree_frame.add_widget(self.data_tree)

    def export_csv(self):
        try:
            self.export.export_data()
        except Exception as expt:
            toast(str(expt))
        else:
            self.export_dialog.dismiss()
            snackbar = Snackbar(text=f'PCD exportado para {self.export.new_file}',duration=10)
            snackbar.show()

    def confirm_export_dialog(self):
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
        if reset:
            self.btn_icon = ['unfold-more-horizontal','unfold-less-horizontal']
            self.btn_text = ['Expandir Árvore', 'Retrair Árvore']
        else:
            self.btn_icon[0], self.btn_icon[1] = self.btn_icon[1], self.btn_icon[0]
            self.btn_text[0], self.btn_text[1] = self.btn_text[1], self.btn_text[0]