from setuptools import setup

APP_NAME = "Detector"
APP = ['printphoto.py']

DATA_FILES = []


OPTIONS = {
    'includes': ['PIL', 'watchdog'],
    'iconfile': 'alert.icns',
    'plist': {
        'CFBundleName': APP_NAME,
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)