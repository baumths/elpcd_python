from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.app import MDApp

import kivy.properties as prop

from lib.data_cls import ManageData, delete_row

Builder.load_file('./lib/kv/data_management.kv')

class DataManagement(MDBoxLayout):

    app = None
    view_only = prop.BooleanProperty()
    item_data = prop.DictProperty()
    delete_dialog = prop.ObjectProperty()
    new_cls = prop.BooleanProperty()
    editing = prop.BooleanProperty(False)

    def __init__(self,view_only=True,item_data=None,new_cls=False,**kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.view_only = view_only
        self.item_data = item_data
        self.new_cls = new_cls
        self.set_fields()
        self.add_buttons()
    
    def set_fields(self):
        if self.view_only:
            self.populate_fields()
        else:
            if self.new_cls:
                self.ids.label_icon.icon = 'folder-plus-outline'
                self.ids.cls_sub.text = 'Nenhuma'
            else:
                self.ids.cls_sub.text = self.item_data['cls_codigo']

    def add_buttons(self):
        if self.view_only:
            buttons = ViewButtons(edit_code=str(self.item_data['cls_codigo']))
        else:
            buttons = EditButtons()
        self.ids.btn_frame.clear_widgets()
        self.ids.btn_frame.add_widget(buttons)

    def enable_edit(self):
        toast(f'Editando {self.item_data["cls_nome"][:40]}{" [...]" if len(self.item_data["cls_nome"]) > 40 else ""}',1)
        self.ids.add_label.text = f'Editando [b]{self.item_data["cls_nome"]}[/b]'
        self.editing = True
        self.view_only = False
        self.add_buttons()

    def populate_fields(self):
        self.ids.add_label.text = f'Visualizando [b]{self.item_data["cls_nome"]}[/b]'
        self.ids.cls_nome.text = str(self.item_data['cls_nome'])
        self.ids.cls_codigo.text = str(self.item_data['cls_codigo'])
        self.ids.cls_sub.text = str(self.item_data['cls_sub']) if self.item_data['cls_sub'] != '' else 'Nenhuma'
        self.ids.reg_abertura.text = str(self.item_data['reg_abertura'])
        self.ids.reg_desativacao.text = str(self.item_data['reg_desativacao'])
        self.ids.reg_reativacao.text = str(self.item_data['reg_reativacao'])
        self.ids.reg_mudanca_nome.text = str(self.item_data['reg_mudanca_nome'])
        self.ids.reg_deslocamento.text = str(self.item_data['reg_deslocamento'])
        self.ids.reg_extincao.text = str(self.item_data['reg_extincao'])
        self.ids.ativa.state = 'down' if self.item_data['cls_indicador'] == 'Ativa' else 'normal'
        self.ids.inativa.state = 'normal' if self.item_data['cls_indicador'] == 'Ativa' else 'down'

    def show_delete_dialog(self):
        btn_cancel = MDFlatButton(
            text='Cancelar',
            theme_text_color='Custom',
            text_color=self.app.theme_cls.primary_dark,
            on_release= lambda x: self.delete_dialog.dismiss())
        btn_confirm = MDRaisedButton(
            text='Apagar',
            elevation= 11,
            on_release= lambda *x: (self.delete_item_from_db(), self.delete_dialog.dismiss()))

        self.delete_dialog = MDDialog(
            title='Deseja realmente apagar?',
            text=f'{self.item_data["cls_nome"]}',
            buttons=[btn_cancel,btn_confirm],
            auto_dismiss=False)
        self.delete_dialog.open()
    
    def delete_item_from_db(self):
        try:
            delete_row(self.item_data)
        except Exception as ihc:
            toast(f'{ihc} Impossível apagar.')
        else:
            toast(f'{self.item_data["cls_nome"][:40]}{" [...]" if len(self.item_data["cls_nome"]) > 40 else ""} apagado com sucesso!')
            self.app.main_frame.ids.data_frame.clear_widgets()
            self.app.pcd_tree.data_tree.delete_node_from_tree()
    
    def text_fields_into_dict(self):
        data = {
            'parentId': self.item_data['legacyId'] if not self.new_cls else 'zero',
            'cls_nome': self.ids.cls_nome.text.strip(),
            'cls_codigo': self.ids.cls_codigo.text.strip(),
            'cls_sub': self.ids.cls_sub.text.strip() if not self.new_cls else '',
            'reg_abertura': self.ids.reg_abertura.text.strip(),
            'reg_desativacao': self.ids.reg_desativacao.text.strip(),
            'reg_reativacao': self.ids.reg_reativacao.text.strip(),
            'reg_mudanca_nome': self.ids.reg_mudanca_nome.text.strip(),
            'reg_deslocamento': self.ids.reg_deslocamento.text.strip(),
            'reg_extincao': self.ids.reg_extincao.text.strip(),
            'cls_indicador': 'Ativa' if self.ids.ativa.state == 'down' else 'Inativa'}
        return data

    def insert_data_into_db(self):
        data = self.text_fields_into_dict()
        parent = self.item_data['legacyId'] if not self.new_cls else 'zero'
        if self.ids.cls_nome.text.strip() and self.ids.cls_codigo.text.strip() != '':
            try:
                to_insert = ManageData(item_data=data,parent_id=parent)
                if not self.editing:
                    to_insert.insert_into_db()
                else:
                    to_insert.update_db()
            except:
                toast('Algo deu errado, impossível salvar a classe!')
            else:
                toast('Classe salva com sucesso!',1)
                self.app.main_frame.ids.data_frame.clear_widgets()
        else:
            toast('Campos obrigatórios estão em branco!')
            self.ids.cls_nome.focus = True if self.ids.cls_nome.text.strip() == '' else False
            self.ids.cls_codigo.focus = True if self.ids.cls_codigo.text.strip() == '' else False
            
    
class EditButtons(MDBoxLayout):
    pass

class ViewButtons(MDBoxLayout):
    def __init__(self,edit_code='',**kwargs):
        super().__init__(**kwargs)
        self.ids.edit_btn.text = f'Editar [b]{edit_code}[/b]'
