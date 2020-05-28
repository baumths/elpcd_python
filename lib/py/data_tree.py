from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.treeview import TreeViewNode
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivymd.app import MDApp

import kivy.properties as prop

class DataTree(MDBoxLayout):
    """Default TreeView object"""
    ## Place holders \/
    app = None ## Main APP reference
    view_only = prop.BooleanProperty() ## View only mode for treeview
    toggled = prop.BooleanProperty(False) ## State of nodes

    def __init__(self, view_only, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app() ## App object reference 
        self.view_only = view_only
        self.populate_all_nodes() ## add nodes to the treeview
    
    def regen_tree(self):
        """Regenerates treeview nodes"""
        self.ids.tree.root.nodes = [] ## clear nodes list
        self.ids.tree.clear_widgets() ## clear treeview widgets
        self.toggled = False ## reset toggled state
        self.populate_all_nodes() ## populate treeview

    def _fetch_data_into_dict(self):
        """Fetches data from database and converts into dict 
        returns a list with a dict for each row of the database
        :return: list"""
        data = self.app.cursor.execute('SELECT * FROM PCD ORDER BY cls_codigo').fetchall()
        description = [ col[0] for col in self.app.cursor.description ]
        return [ dict(zip(description,item)) for item in data ]

    def _create_all_nodes(self):
        """Generates all nodes and sort them between parent and child 
        returns a tupple of (parents,children) lists
        :return: tupple"""
        parents = [] ## parents list
        children = [] ## children list
        data = self._fetch_data_into_dict() ## database items in dict
        for item in data:
            ## Creates treeview node object for each item in database \/
            label = CustomTVLabel(text=f"{item['cls_codigo']} - {item['cls_nome']}")
            label.item_data = item ## add data dict to object
            label.bind(on_touch_down= lambda node,_: self.generate_data_frame(node)) ## bind function
            ## sorting parents and children
            if str(item['parentId']) == 'zero':
                parents.append(label)
            else:
                children.append(label)
        return parents,children

    def populate_all_nodes(self):
        """Populate treeview with new nodes"""
        parents,children = self._create_all_nodes()

        for parent in parents:
            ## add parents to tree
            self.ids.tree.add_node(parent)
        
        ## adds children nodes into parents
        for parent in self.ids.tree.iterate_all_nodes():
            for child in children:
                if parent != self.ids.tree.root: ## skip root node
                    if child.item_data['parentId'] == parent.item_data['legacyId']:
                        self.ids.tree.add_node(child,parent=parent)
                        children.remove(child)
    
    def generate_data_frame(self,node):
        """Creates data management obj from current node data 
        node = instance of selected node
        :param node: obj"""
        if not self.view_only: ## checks if in visualization only mode
            toast(f'Selecionado: {node.text[:40]}{" [...]" if len(node.text) > 40 else ""}',1)
            self.app.set_data_management_widget(view_only=True,item_data=node.item_data)
    
    def delete_node_from_tree(self):
        """Delete selected node from tree"""
        if not self.view_only: ## checks if in visualization only mode
            self.ids.tree.remove_node(self.ids.tree.get_selected_node())
    
    def toggle_all_nodes(self):
        """Toggles all nodes to toggled state"""
        for node in self.ids.tree.iterate_all_nodes():
            if node != self.ids.tree.root:
                if self.toggled and node.is_open:
                    ## close open node
                    self.ids.tree.toggle_node(node)
                if not self.toggled and not node.is_open:
                    ## open closed nodes
                    self.ids.tree.toggle_node(node)
        ## switches toggled state \/
        self.toggled = False if self.toggled else True

class CustomTVLabel(TreeViewNode,MDLabel):
    """Custom node objcet for storing database row"""

    item_data = prop.DictProperty() ## Dict with one row from database

    def __init__(self,**kwargs):
        super().__init__(**kwargs)