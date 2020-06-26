# -*- mode: python ; coding: utf-8 -*-

app_name = 'ElPCD v0.4 Beta'

from kivymd import hooks_path as kivymd_hooks_path

import os
import platform

path = os.path.abspath('.')

datas = [
    (os.path.join(path, 'elpcd.kv'),'.'),
    (os.path.join(path, 'lib', '*.py'), f'lib{os.sep}'),
    (os.path.join(path, 'lib', 'py', '*.py'), f'lib{os.sep}py{os.sep}'),
    (os.path.join(path, 'lib', 'kv', '*.kv'), f'lib{os.sep}kv{os.sep}'),
    (os.path.join(path, 'assets', '*.png'), f'assets{os.sep}'),
    ]

a = Analysis(
    ['main.py'],
    pathex=[path],
    binaries=[],
    datas=datas,
    hiddenimports=[
       'kivymd.uix.managerswiper',
       'kivymd.uix.datatables',
       'kivymd.stiffscroll'
       ],
    hookspath=[kivymd_hooks_path],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
    )
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None
    )
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=os.path.join(path, 'elpcd192x.ico')
    )

if platform.system() == 'Windows':
    from kivy_deps import glew, angle, sdl2
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        *[Tree(p) for p in (glew.dep_bins + angle.dep_bins + sdl2.dep_bins)],
        strip=False,
        upx=True,
        )
