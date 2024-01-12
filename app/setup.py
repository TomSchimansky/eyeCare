
from setuptools import setup
from settings import Settings

APP = ['main.py']

OPTIONS = {'argv_emulation': False,
           'iconfile': 'assets/images/GuitarTunerDesign.icns',
           'plist': {
               'CFBundleName': Settings.APP_NAME,
               'CFBundleDisplayName': Settings.APP_NAME,
               'CFBundleExecutable': Settings.APP_NAME,
               'CFBundleGetInfoString': "Tune your guitar the most simplest way.",
               'CFBundleIdentifier': "com.TomSchimansky.GuitarTuner",
               'CFBundleVersion': Settings.VERSION,
               'CFBundleShortVersionString': Settings.VERSION,
               'NSHumanReadableCopyright': u"Copyright © 2020, Tom Schimansky, All Rights Reserved"
           }}

setup(
    name=APP_NAME,
    app=APP,
    author='Tom Schimansky',
    data_files=[("assets/images", IMAGE_FILES),
                ("assets/sounds", SOUND_FILES)],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
