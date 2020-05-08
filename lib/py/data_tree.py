from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.treeview import TreeViewNode
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.app import MDApp

import kivy.properties as prop

Builder.load_file('./lib/kv/data_tree.kv')

class DataTree(MDBoxLayout):

    app = None
    view_only = prop.BooleanProperty()
    toggled = prop.BooleanProperty(False)

    def __init__(self, view_only, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.view_only = view_only
        self.populate_all_nodes()
    
    def regen_tree(self):
        self.ids.tree.root.nodes = []
        self.ids.tree.clear_widgets()
        self.populate_all_nodes()

    def _fetch_data_into_dict(self):
        data = self.app.cursor.execute('SELECT * FROM PCD ORDER BY cls_codigo').fetchall()
        description = [ col[0] for col in self.app.cursor.description ]
        return [ dict(zip(description,item)) for item in data ]

    def _create_all_nodes(self):
        parents = []
        children = []
        data = self._fetch_data_into_dict()
        for item in data:
            label = CustomTVLabel(text=f"{item['cls_codigo']} - {item['cls_nome']}")
            label.item_data = item
            label.bind(on_touch_down= lambda node,_: self.generate_data_frame(node))
            if str(item['parentId']) == 'zero':
                parents.append(label)
            else:
                children.append(label)
        return parents,children

    def populate_all_nodes(self):
        parents,children = self._create_all_nodes()

        for parent in parents:
            self.ids.tree.add_node(parent)
        
        for parent in self.ids.tree.iterate_all_nodes():
            for child in children:
                if parent != self.ids.tree.root:
                    if child.item_data['parentId'] == parent.item_data['legacyId']:
                        self.ids.tree.add_node(child,parent=parent)
                        children.remove(child)
    
    def generate_data_frame(self,node):
        if not self.view_only:
            toast(f'Selecionado: {node.text[:40]}{" [...]" if len(node.text) > 40 else ""}',1)
            self.app.set_data_management_widget(view_only=True,item_data=node.item_data)
    
    def delete_node_from_tree(self):
        if not self.view_only:
            self.ids.tree.remove_node(self.ids.tree.get_selected_node())
    
    def toggle_all_nodes(self):
        for node in self.ids.tree.iterate_all_nodes():
            if node != self.ids.tree.root:
                if self.toggled and node.is_open:
                    self.ids.tree.toggle_node(node)
                if not self.toggled and not node.is_open:
                    self.ids.tree.toggle_node(node)
        self.toggled = False if self.toggled else True

class CustomTVLabel(TreeViewNode,MDLabel):

    item_data = prop.DictProperty()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)