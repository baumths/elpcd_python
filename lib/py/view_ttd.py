from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.metrics import dp

import lib.gen_ref_code

def view_ttd():
    """Create and open datatable dialog popup"""
    app = MDApp.get_running_app() ## main app object reference
    data = lib.gen_ref_code.generate_reference_codes()
    ## create data rows for datatable \/
    table_data = [ (
        item['codigo_ref'],
        f"{item['cls_nome'][:60]}{' [ . . . ]' if len(item['cls_nome']) > 60 else ''}",
        item['fase_corrente'] if item['fase_corrente'].strip() != '' else '-',
        item['fase_intermediaria'] if item['fase_corrente'].strip() != '' else '-',
        item['dest_final']) for item in data ]

    datatable = MDDataTable(
            size_hint = (0.95, 0.9),
            column_data = [
                ("Código de Referência", dp(40)),
                ("Nome da Classe", dp(95)),
                ("Fase Corrente", dp(30)),
                ("Fase Intermediária", dp(40)),
                ("Destinação Final", dp(30))
            ],
            rows_num = len(table_data) if len(table_data) > 0 else 1,
            row_data = table_data
        )
    datatable.bind(on_dismiss= lambda *x: app.root.switch_to_screen('pcd'))
    datatable.open()