# -*- mode: python -*-
# vim: ft=python

block_cipher = None

a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('omnis_wsbus/ssl', 'ssl'),
        ('omnis_wsbus/ssl_root', 'ssl_root'),
        ('omnis_wsbus/templates', 'templates'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='omnis-wsbus',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True
)
