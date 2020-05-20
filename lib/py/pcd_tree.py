from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder

import kivy.properties as prop

from lib.py.data_tree import DataTree

Builder.load_file('./lib/kv/pcd_tree.kv')

class PCDTree(MDBoxLayout):

    data_tree = prop.ObjectProperty() ## treeview object place holder
    btn_icon = prop.ListProperty(['unfold-more-horizontal','unfold-less-horizontal'])
    btn_text = prop.ListProperty(['Expandir Árvore', 'Retrair Árvore'])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tree = DataTree(view_only=False) ## treeview object
        self.ids.tree_frame.add_widget(self.data_tree) ## add treeview to screen
    
    def switch_button(self,reset=False):
        """Switches tooltip and icon when pressed"""
        if reset:
            self.btn_icon = ['unfold-more-horizontal','unfold-less-horizontal']
            self.btn_text = ['Expandir Árvore', 'Retrair Árvore']
        else:
            self.btn_icon[0], self.btn_icon[1] = self.btn_icon[1], self.btn_icon[0]
            self.btn_text[0], self.btn_text[1] = self.btn_text[1], self.btn_text[0]