# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import os

a = Analysis([os.path.join(os.getcwd(),'gui.py')],#script
             pathex=['.'], #Where to put the bundled app (default: ./dist)
             binaries=[],
             datas=[],
             hiddenimports=['iocbio.kinetics.calc.bump','iocbio.kinetics.calc.composer', 'iocbio.kinetics.calc.current', 'iocbio.kinetics.calc.explin_fit', 'iocbio.kinetics.calc.generic', 'iocbio.kinetics.calc.linreg', 'iocbio.kinetics.calc.mean_med_std', 'iocbio.kinetics.calc.mm', 'iocbio.kinetics.calc.xy', 'iocbio.kinetics.global_vars', 'iocbio.kinetics.constants', 'iocbio.kinetics.io.data', 'msgpack'],# Name an import not visible in the code of the script(s). 
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='gui', # app name
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app') # Folder name where all needed is stored
