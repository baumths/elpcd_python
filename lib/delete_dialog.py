from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivymd.app import MDApp

import lib.data_cls

class CustomTooltipIconButton(MDTooltip,MDIconButton):
    pass

def delete_dialog():
    app = MDApp.get_running_app()
    dialog = MDDialog(
        auto_dismiss=False,
        title= 'Deseja APAGAR seu PCD inteiro?',
        text= 'Ação NÃO poderá ser desfeita!',
        buttons=[
            MDRaisedButton(
                elevation= 11,
                text = 'Cancelar',
                theme_text_color='Custom',
                text_color= app.theme_cls.bg_light,
                md_bg_color= app.theme_cls.primary_dark,
                on_release= lambda x: dialog.dismiss()
            ),
            CustomTooltipIconButton(
                icon= 'delete',
                tooltip_text= 'Impossível Desfazer!',
                theme_text_color= 'Custom',
                text_color= (1,0,0,1),
                pos_hint= {'center_y': .4},
                on_release= lambda x: (_delete_table(),dialog.dismiss())
            )
        ]
    )
    dialog.open()

def _delete_table():
    app = MDApp.get_running_app()
    try:
        lib.data_cls.drop_table('PCD')
    except Exception as expt:
        toast(str(expt))
    else:
        toast('PCD apagado com sucesso!')
        app.pcd_tree.data_tree.regen_tree()