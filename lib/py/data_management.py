from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivymd.app import MDApp

import kivy.properties as prop

from lib.data_cls import ManageData, delete_row
import lib.utils

class DataManagement(MDBoxLayout):
    """Object of text fields and buttons for managing data"""

    ## Place holders \/
    app = None ## Main APP reference
    item_data = prop.DictProperty() ## Dict of one row from database
    new_cls = prop.BooleanProperty() ## Bool for new item without parents
    view_only = prop.BooleanProperty() ## Enables/Disables text fields
    delete_dialog = prop.ObjectProperty() ## Delete Dialog popup object
    editing = prop.BooleanProperty(False) ## Enable/Disable editing mode

    def __init__(self,view_only=True,item_data=None,new_cls=False,**kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app() ## App object reference
        self.view_only = view_only
        self.item_data = item_data
        self.new_cls = new_cls
        self.set_fields() ## Set text field contents
        self.add_buttons() ## Add buttons to screen
    
    def set_fields(self):
        """Set rules for text fields content"""
        if self.view_only:
            ## populate fields with current database row
            self.populate_fields()
        else:
            ## if not view_only tests for new item 
            if self.new_cls:
                ## if new item, changes label icon and adds 'None' to parent node
                self.ids.label_icon.icon = 'folder-plus-outline'
                self.ids.cls_sub.text = '[ Fundo ]'
                self.app.pcd_tree.disabled = True ## Locks treeview
            else:
                ## if not new item, adds current item code as item parent
                self.ids.cls_sub.text = self.item_data['cls_codigo']

    def add_buttons(self):
        """Add buttons depending on view_only mode"""
        if self.view_only:
            buttons = ViewButtons(edit_code=str(self.item_data['cls_codigo']))
        else:
            buttons = EditButtons()
        self.ids.btn_frame.clear_widgets()
        self.ids.btn_frame.add_widget(buttons)

    def enable_edit(self):
        """Enables editing of text fields"""
        toast(f'Editando {self.item_data["cls_nome"][:40]}{" [...]" if len(self.item_data["cls_nome"]) > 40 else ""}',1)
        self.ids.add_label.text = f'[b]Editando[/b] {self.item_data["cls_nome"]}'
        self.editing = True ## Enables editing
        self.view_only = False ## Disables view_only mode
        self.app.pcd_tree.disabled = True ## Locks treeview
        self.add_buttons() ## Add new buttons

    def populate_fields(self):
        """Populates text fields with current item_data data"""
        self.ids.add_label.text = f'Visualizando [b]{self.item_data["cls_nome"]}[/b]'
        self.ids.cls_nome.text = str(self.item_data['cls_nome'])
        self.ids.cls_codigo.text = str(self.item_data['cls_codigo'])
        self.ids.cls_sub.text = str(self.item_data['cls_sub']) if self.item_data['cls_sub'] != '' else '[ Fundo ]'
        self.ids.reg_abertura.text = str(self.item_data['reg_abertura'])
        self.ids.reg_desativacao.text = str(self.item_data['reg_desativacao'])
        self.ids.reg_reativacao.text = str(self.item_data['reg_reativacao'])
        self.ids.reg_mudanca_nome.text = str(self.item_data['reg_mudanca_nome'])
        self.ids.reg_deslocamento.text = str(self.item_data['reg_deslocamento'])
        self.ids.reg_extincao.text = str(self.item_data['reg_extincao'])
        self.ids.ativa.state = 'down' if self.item_data['cls_indicador'] == 'Ativa' else 'normal'
        self.ids.inativa.state = 'normal' if self.item_data['cls_indicador'] == 'Ativa' else 'down'
        self.ids.fase_corrente.text = str(self.item_data['fase_corrente'])
        self.ids.evento_fase_corrente.text = str(self.item_data['evento_fase_corrente'])
        self.ids.fase_intermediaria.text = str(self.item_data['fase_intermediaria'])
        self.ids.evento_fase_inter.text = str(self.item_data['evento_fase_inter'])
        self.ids.preservacao.state = 'down' if self.item_data['dest_final'] == 'Preservação' else 'normal'
        self.ids.eliminacao.state = 'normal' if self.item_data['dest_final'] == 'Preservação' else 'down'
        self.ids.reg_alteracao.text = str(self.item_data['reg_alteracao'])
        self.ids.observacoes.text = str(self.item_data['observacoes'])

    def show_delete_dialog(self):
        """Create and open delete dialog popup"""
        btn_cancel = MDFlatButton(
            text = 'Cancelar',
            theme_text_color = 'Custom',
            text_color = self.app.theme_cls.primary_color,
            on_release = lambda x: self.delete_dialog.dismiss())
        btn_confirm = MDRaisedButton(
            text = 'Apagar',
            elevation = 11,
            on_release = lambda *x: (self.delete_item_from_db(), self.delete_dialog.dismiss()))

        self.delete_dialog = MDDialog(
            title = 'Deseja realmente apagar?',
            text = f'{self.item_data["cls_nome"]}',
            buttons = [btn_cancel,btn_confirm],
            auto_dismiss = False)
        self.delete_dialog.open()
    
    def delete_item_from_db(self):
        """Try deleting item from database, if successful, deletes item from treeview"""
        try:
            delete_row(self.item_data)
        except lib.utils.ItemHasChildren:
            toast('Classe possui dependentes! Impossível apagar.')
        else:
            toast(f'{self.item_data["cls_nome"][:40]}{" [...]" if len(self.item_data["cls_nome"]) > 40 else ""} apagado com sucesso!',1)
            self.app.root.ids.data_frame.clear_widgets() ## clear data management frame
            self.app.pcd_tree.delete_node_from_tree() ## delete item from treeview
    
    def text_fields_into_dict(self):
        """Gets data from text fields into dict
        :return: dict"""
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
            'cls_indicador': 'Ativa' if self.ids.ativa.state == 'down' else 'Inativa',
            'fase_corrente': self.ids.fase_corrente.text.strip(),
            'evento_fase_corrente': self.ids.evento_fase_corrente.text.strip(),
            'fase_intermediaria': self.ids.fase_intermediaria.text.strip(),
            'evento_fase_inter': self.ids.evento_fase_inter.text.strip(),
            'dest_final': 'Preservação' if self.ids.preservacao.state == 'down' else 'Eliminação',
            'reg_alteracao': self.ids.reg_alteracao.text.strip(),
            'observacoes': self.ids.observacoes.text.strip()}
        return data
    
    def insert_data_into_db(self):
        """Try to insert data into database,
        if successful regen treeview with new data"""
        data = self.text_fields_into_dict() ## Current item data dict
        parent = self.item_data if not self.new_cls else 'zero' ## set parent data if not new cls
        if self.ids.cls_nome.text.strip() and self.ids.cls_codigo.text.strip() != '':
            ## if required fields are not empty
            try:
                ## Instantiate data manager object \/
                to_insert = ManageData(item_data=data,parent_data=parent)
                if not self.editing:
                    to_insert.insert_into_db() ## inserts into database
                else:
                    to_insert.update_db() ## updates database
            except:
                toast('Algo deu errado! Impossível salvar a Classe.')
            else:
                toast('Classe salva com sucesso!',1)
                self.app.root.ids.data_frame.clear_widgets() ## clear data management frame 
                self.app.pcd_tree.regen_tree() ## Regenerates pcd treeview
                self.app.pcd_tree.switch_button(reset=True) ## switch toggle nodes button
                self.app.pcd_tree.disabled = False ## Unlocks treeview
        else:
            ## if required fields are empty
            toast('Campos obrigatórios estão em branco!')
            self.ids.cls_codigo.focus = True if self.ids.cls_codigo.text.strip() == '' else False
            self.ids.cls_nome.focus = True if self.ids.cls_nome.text.strip() == '' else False
    
class EditButtons(MDBoxLayout):
    """Editing buttons (save, cancel)"""
    pass

class ViewButtons(MDBoxLayout):
    """Visualization buttons (edit, add_new, delete, cancel)"""

    app = prop.ObjectProperty() ## App instance

    def __init__(self, edit_code = '', **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.ids.edit_btn.text = f'Editar [b]{edit_code}[/b]' ## sets edit button text

    def add_btn_callback(self):
        self.app.set_data_management_widget(
            view_only = False,
            item_data = self.app.data_management.item_data,
            new_cls = False
            )
        self.app.pcd_tree.disabled = True ## Locks treeview
