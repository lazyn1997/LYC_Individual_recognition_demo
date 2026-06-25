# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

block_cipher = None

# Get site-packages path
site_packages = None
for path in sys.path:
    if 'site-packages' in path and os.path.exists(path):
        site_packages = Path(path)
        break

if site_packages is None:
    raise Exception("Could not find site-packages directory!")

# Collect paddlepaddle DLLs and data
paddle_path = site_packages / 'paddle'
paddle_bin = []
paddle_datas = []

if paddle_path.exists():
    # Collect all .dll files from paddle
    for dll in paddle_path.rglob('*.dll'):
        paddle_bin.append((str(dll), '.'))
    
    # Collect other necessary files
    for pat in ['*.so', '*.pyd', '*.dll']:
        for f in paddle_path.rglob(pat):
            if f not in [x[0] for x in paddle_bin]:
                paddle_bin.append((str(f), '.'))
    
    # Collect paddle data files
    for data_dir in ['libs', 'include', 'third_party']:
        data_path = paddle_path / data_dir
        if data_path.exists():
            for f in data_path.rglob('*'):
                if f.is_file():
                    rel_path = f.relative_to(paddle_path)
                    paddle_datas.append((str(f), str(rel_path.parent)))

a = Analysis(
    ['scripts\\predict.py'],
    pathex=[],
    binaries=paddle_bin,
    datas=paddle_datas,
    hiddenimports=[
        'paddle',
        'paddle.fluid',
        'paddle.fluid.core',
        'paddle.inference',
        'cv2',
        'faiss',
        'numpy',
        'yaml',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='predict',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='predict',
)
