# -*- mode: python ; coding: utf-8 -*-

VERSION = '0.0.0.1'

a = Analysis(
    ['dualImgView.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('dualImgView.ico','.'),
        ('LICENSE', '.'),
        ('README.md', '.'),
        ('3rdparty-licenses/PySide6/COPYING.LGPLv3','3rdparty-licenses/PySide6'),
        ('3rdparty-licenses/PySide6/COPYING.GPLv3','3rdparty-licenses/PySide6'),
        ('3rdparty-licenses/PySide6/NOTICE-PySide6.txt','3rdparty-licenses/PySide6'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # GUI-Frameworks (nicht PySide6)
        'tkinter', 'turtle', 'pygame',
        
        # Web-bezogene Module
        'flask', 'django', 'werkzeug', 'jinja2',
        'requests', 'urllib3', 'http.server', 'xmlrpc',
        
        # Wissenschaftliche Bibliotheken
        'numpy', 'scipy', 'matplotlib', 'pandas', 'sympy',
        'IPython', 'jupyter', 'notebook',
        
        # Datenbanken
        'sqlite3', 'mysql', 'postgresql',
        
        # Testing/Debugging
        'unittest', 'doctest', 'pdb', 'cProfile', 'profile',
        
        # Ungenutzte PySide6 Module
        'PySide6.QtNetwork', 'PySide6.QtWebEngine', 'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebChannel', 'PySide6.QtWebSockets', 'PySide6.QtSql',
        'PySide6.QtMultimedia', 'PySide6.QtMultimediaWidgets',
        'PySide6.Qt3DCore', 'PySide6.Qt3DRender', 'PySide6.Qt3DInput',
        'PySide6.QtCharts', 'PySide6.QtDataVisualization', 'PySide6.QtQuick',
        'PySide6.QtQuickControls2', 'PySide6.QtQuickWidgets', 'PySide6.QtQml',
        'PySide6.QtDesigner', 'PySide6.QtHelp', 'PySide6.QtTest',
        'PySide6.QtConcurrent', 'PySide6.QtSerialPort', 'PySide6.QtBluetooth',
        'PySide6.QtOpenGL', 'PySide6.QtOpenGLWidgets', 'PySide6.QtSvg',
        
        # Compiler/Build Tools
        'distutils', 'setuptools', 'wheel', 'pip',
    ],
    noarchive=False,
    optimize=2,
    cipher=None,
)

pyz = PYZ(a.pure,
    cipher=None,
    exclude_packages=[
        'unittest', 'doctest', 'pdb',
        'distutils', 'setuptools',
    ],
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Dual-Image Viewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[
        '*.dll', 'python*.dll', 'Qt6*.dll'
    ],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='dualImgView.ico',
    version='file_version_info.txt',
    uac_admin=False,
    uac_uiaccess=False,
    manifest=None,
    resources=[],
    hides_console=True,
    exclude_binaries=False,
    contents_directory='.',
)
