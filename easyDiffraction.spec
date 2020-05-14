# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/Users/andrewsazonov/Development/Projects/easyDiffraction/easyDiffraction/App/easyDiffraction.py'],
             pathex=['/Users/andrewsazonov/Development/Projects/easyDiffraction/easyDiffraction'],
             binaries=[],
             datas=[('/Users/andrewsazonov/Development/Projects/easyDiffraction/easyDiffraction/.venv/lib/python3.7/site-packages/cryspy', 'cryspy'), ('/Users/andrewsazonov/Development/Projects/easyDiffraction/easyDiffraction/App', '.')],
             hiddenimports=[],
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
          name='easyDiffraction',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='/Users/andrewsazonov/Development/Projects/easyDiffraction/easyDiffraction/App/QmlImports/easyDiffraction/Resources/Icons/App.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='easyDiffraction')
app = BUNDLE(coll,
             name='easyDiffraction.app',
             icon='/Users/andrewsazonov/Development/Projects/easyDiffraction/easyDiffraction/App/QmlImports/easyDiffraction/Resources/Icons/App.icns',
             bundle_identifier=None)
