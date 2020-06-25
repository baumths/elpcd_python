from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivymd.app import MDApp

import lib.data_cls
import lib.utils

class CustomTooltipIconButton(MDTooltip, MDIconButton):
    pass

def delete_dialog():
    """Create and open delete dialog popup for deleting the entire database table"""
    app = MDApp.get_running_app() ## App object reference
    dialog = MDDialog(
        auto_dismiss = False,
        title = 'Deseja APAGAR seu PCD inteiro?',
        text = 'Ação NÃO poderá ser desfeita!',
        buttons = [
            CustomTooltipIconButton(
                icon = 'delete',
                tooltip_text = 'Impossível Desfazer!',
                theme_text_color = 'Custom',
                text_color = (1,0,0,1),
                pos_hint = {'center_y': .4},
                on_release = lambda _: (_delete_table(),dialog.dismiss())
            ),
            MDRaisedButton(
                elevation = 10,
                text = 'Cancelar',
                theme_text_color = 'Custom',
                text_color = app.theme_cls.bg_light,
                md_bg_color = app.theme_cls.primary_color,
                on_release = lambda _: dialog.dismiss()
            )
        ]
    )
    dialog.open()

def _delete_table():
    """Callback for deleting database table"""
    app = MDApp.get_running_app() ## App object reference
    try:
        lib.data_cls.drop_table()
    except lib.utils.NotAbleToDeleteDB:
        toast('Impossível apagar dados!', 1)
    else:
        toast('PCD apagado com sucesso!', 2)
        app.pcd_tree.regen_tree() ## regens tree after droping table
        app.root.ids.data_frame.clear_widgets() ## clears form widget
        app.pcd_tree.disabled = False ## Unlocks treeview