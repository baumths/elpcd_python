from kivymd.uix.behaviors import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.treeview import TreeViewNode
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.app import MDApp

import kivy.properties as prop

from ..gen_ref_code import _build_reference_code
from .data_management import DataManagement

class CustomTVLabel(HoverBehavior, TreeViewNode, MDLabel):
    """Custom node object for storing database row"""

    item_data = prop.DictProperty() ## Dict with one row from database

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class PCDTree(MDBoxLayout):
    """Treeview widget + buttons and dialogs
    manipulations refered to data"""

    btn_icon = prop.ListProperty(['unfold-more-horizontal','unfold-less-horizontal'])
    btn_text = prop.ListProperty(['Expandir Árvore', 'Retrair Árvore'])

    app = prop.ObjectProperty() ## Main APP reference
    toggled = prop.BooleanProperty(False) ## State of nodes
    nodes_dict = prop.DictProperty() ## All nodes instances callable via id

    dialog = prop.ObjectProperty() ## Search dialog
    search_widget = prop.ObjectProperty() ## Search dialog content instance
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.populate_all_nodes() ## add nodes to the treeview

        self.search_widget = SearchFrame(self) ## creates search widget
        self.create_search_dialog() ## creates search dialog with `self.search_widget`
    """
    Treeview methods
    """
    def regen_tree(self):
        """Regenerates treeview nodes"""
        self.ids.treeview.root.nodes = [] ## clear nodes list
        self.ids.treeview.clear_widgets() ## clear nodes widgets
        self.toggled = False ## reset toggled state
        self.populate_all_nodes() ## populate treeview

    def _fetch_data_into_dict(self):
        """Fetches data from database and converts into dict 
        returns a list with a dict for each row of the database
        :return: list"""
        query = 'SELECT * FROM PCD ORDER BY cls_codigo'
        data = self.app.cursor.execute(query).fetchall()
        description = [ col[0] for col in self.app.cursor.description ]
        return [ dict(zip(description,item)) for item in data ]

    def _create_all_nodes(self):
        """Generates all nodes and sorts them between parents and
        children, returns a tupple of (parents,children) lists
        :return: tupple"""
        self.nodes_dict = {} ## nodes instances for future reference
        parents = [] ## parents list
        children = [] ## children list
        data = self._fetch_data_into_dict() ## database items in dict
        for item in data:
            ## Creates treeview node object for each item in database \/
            label = CustomTVLabel(text=f"{item['cls_codigo']} - {item['cls_nome']}")
            label.item_data = item ## add data dict to object
            label.bind(on_touch_down= lambda node, _: self._node_callback(node)) ## bind function
            ## Adding reference to dict
            self.nodes_dict[item['legacyId']] = label
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
            self.ids.treeview.add_node(parent)
        
        ## adds children nodes into parents
        for parent in self.ids.treeview.iterate_all_nodes():
            for child in children:
                if parent != self.ids.treeview.root: ## skip root node
                    if child.item_data['parentId'] == parent.item_data['legacyId']:
                        self.ids.treeview.add_node(child,parent=parent)
                        children.remove(child)
    
    def _node_callback(self, node):
        """Callback for treeview nodes, checks if
        Form isn't already the selected node
        :param node: obj"""
        df_c = self.app.root.ids.data_frame.children
        if df_c and isinstance(df_c[0], DataManagement):
            ## Form exists
            if df_c[0].item_data['legacyId'] == node.item_data['legacyId']:
                ## Node is IN the current Form
                return
        ## Form doesn't exist or node != current node
        self.generate_data_frame(node)

    def generate_data_frame(self, node):
        """Creates data management obj from current
        node data. node = instance of selected node
        :param node: obj"""
        self.app.set_data_management_widget(
                view_only = True,
                item_data = node.item_data
                )
    
    def delete_node_from_tree(self):
        """Delete selected node from tree"""
        selected_node = self.ids.treeview.get_selected_node()
        self.ids.treeview.remove_node(selected_node)
        self.nodes_dict.pop(selected_node.item_data['legacyId'])
    """
    Buttons methods
    """
    def toggle_all_nodes(self):
        """Toggles all nodes to toggled state"""
        for node in self.ids.treeview.iterate_all_nodes():
            if node != self.ids.treeview.root:
                if self.toggled and node.is_open:
                    ## close open node
                    self.ids.treeview.toggle_node(node)
                if not self.toggled and not node.is_open:
                    ## open closed nodes
                    self.ids.treeview.toggle_node(node)
        ## switches toggled state \/
        self.toggled = not self.toggled
    
    def switch_button(self,reset=False):
        """Switches tooltip and icon when pressed"""
        if reset:
            self.btn_icon = ['unfold-more-horizontal','unfold-less-horizontal']
            self.btn_text = ['Expandir Árvore', 'Retrair Árvore']
        else:
            self.btn_icon[0], self.btn_icon[1] = self.btn_icon[1], self.btn_icon[0]
            self.btn_text[0], self.btn_text[1] = self.btn_text[1], self.btn_text[0]
    """
    Search dialog methods
    """
    def create_search_dialog(self):
        """Creates search dialog"""
        if not self.dialog:
            self.dialog = MDDialog(
                title = 'Clique na Classe para encontrá-la na árvore',
                size_hint = (.5,.9),
                pos_hint = {'right': .9},
                overlay_color = [0, 0, 0, .3],
                auto_dismiss = False,
                type = "custom",
                radius = [20,],
                content_cls = self.search_widget)
            self.dialog.bind(on_open = self.set_focus)

    def set_focus(self, *_):
        """Sets focus to text field"""
        self.search_widget.ids.to_search.focus = True

class SearchFrame(MDBoxLayout):
    """Search widgets container to be added to dialog"""

    ## List used by recycleview to populate nodes
    data = prop.ListProperty()

    ## MDDialog caller to dismiss later
    pcd_tree = prop.ObjectProperty()
    ## Reference to the treeview itself
    treeview = prop.ObjectProperty()
    
    def __init__(self, caller, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.pcd_tree = caller

        self.results = self.ids.search_results ## reference to recycleview
        self.treeview = self.pcd_tree.ids.treeview
        self.regen_search_data()
    
    def collect_data(self):
        """Fetches data from database to populate recycleview
        :return: list"""
        query = 'SELECT legacyId, parentId, cls_codigo, cls_nome FROM PCD ORDER BY cls_codigo'
        table = self.app.cursor.execute(query).fetchall()
        description = [ col[0] for col in self.app.cursor.description]
        return [ dict(zip(description, item)) for item in table ]

    def _gen_data(self):
        """Generates a list of dicts and returns it
        :return: list"""
        table = [ {'codigo_ref':_build_reference_code(row), **row} for row in self.collect_data() ]
        row_to_dict = lambda item: {
            'search_frame': self,
            'codigo_ref': item['codigo_ref'],
            'cls_nome': item['cls_nome'],
            'legacyId': item['legacyId']
            }
        return [ row_to_dict(item) for item in table ]
    
    def refresh(self):
        """Refreshes recycleview and sets scroll to top"""
        self.results.refresh_from_data()
        self.results.scroll_y = 1
    
    def regen_search_data(self):
        """Regenerates recycleview data"""
        self.data = self._gen_data() ## gather data to recycleview
        self.results.data = self.data
        self.refresh()

    def find_nodes(self, text):
        """Traverses `self.data` list and
        sorts out nodes that don't match `text`
        :param text: str"""
        if text.strip() == '': ## if search is empty
            self.regen_search_data()
        else:
            ## Lambda to make list comprehension shorter
            to_find = lambda item: (item['codigo_ref']+' '+item['cls_nome'])
            ## Filtering data according to search text
            self.results.data = [ item for item in self.data if text.strip() in to_find(item) ]
            ## Refreshing recycleview and sending scroll up to the top data 
            self.refresh()

    def node_callback(self, node):
        """Called when user clicks on a node
        :param node: obj"""
        self.pcd_tree.dialog.dismiss() ## close dialog
        ## schedule text clearing
        def clear_search_field(*_):
            self.ids.to_search.text = ''
        Clock.schedule_once(clear_search_field, .25)
        ## selects node in treeview
        self.select_node_in_tree(node)
    
    def select_node_in_tree(self, node):
        """Selects searched node in treeview
        :param node: obj"""
        ## gets selected_node instance in treeview
        selected_node = self.pcd_tree.nodes_dict[node.legacyId]
        ## opens closed treeviewnodes
        self.cascade_tree_nodes(selected_node)
        ## selects node in treeview
        self.treeview.select_node(selected_node)
        ## dispatch click onto node
        selected_node.dispatch('on_touch_down', None)
    
    def cascade_tree_nodes(self, node):
        """Recursive function to open all
        parent nodes on treeview
        :param node: obj"""
        if node.item_data['parentId'] == 'zero': ## base case
            if not node.is_open:
                self.treeview.toggle_node(node) ## toggles root node
        else:
            ## toggles from deepest node up until it reaches root node
            self.cascade_tree_nodes(self.pcd_tree.nodes_dict[node.item_data['parentId']])
            if not node.is_open:
                self.treeview.toggle_node(node)

class SearchNode(ButtonBehavior, HoverBehavior, MDBoxLayout):
    """Custom widget to populate recycleview"""

    cls_nome = prop.StringProperty() ## Node name
    codigo_ref = prop.StringProperty() ## Node reference rode
    legacyId = prop.NumericProperty() ## Node id to be searched
    search_frame = prop.ObjectProperty() ## Root widget reference

    def on_enter(self, *args):
        """Mouse over node, bg color becomes gray"""
        self.md_bg_color = [.8, .8, .8, .8]

    def on_leave(self, *args):
        """Mouse leaves node, bg color back to default"""
        self.md_bg_color = [1, 1, 1, 1]