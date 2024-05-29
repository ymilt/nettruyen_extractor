# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['follow.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['ujson', 'curl_cffi', 'browser_cookie3', 'win32crypt', 'Crypto.Cipher.AES', 'concurrent.futures'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='follow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['nettruyen.ico'],
)
