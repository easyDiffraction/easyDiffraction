#!/bin/sh
clear

CURRENT_DIR="$(dirname "$0")"
VENV_DIR=$CURRENT_DIR/.python-venv

echo "*** activate virtual environment: $VENV_DIR"
source $VENV_DIR/bin/activate

echo "*** python info"
which python
python --version

echo "*** go to project dir"
cd $CURRENT_DIR

echo "*** run pyinstaller"
#pyinstaller \
#--noconfirm \ # -y, --noconfirm. Replace output directory without asking for confirmation
#--clean \ # Clean PyInstaller cache and remove temporary files before building.
#--windowed \ # -w, --windowed, --noconsole. Windows and Mac OS X: do not provide a console window for standard i/o.
#--onedir \ # -D, --onedir. Create a one-folder bundle containing an executable
#--onefile \ # -F, --onefile. Create a one-file bundled executable.
#--log-level ERROR \ # log levels TRACE, DEBUG, INFO, WARN, ERROR, CRITICAL (default: INFO).
#$PROJECT_NAME.py
##pyinstaller easyDiffraction.spec --noconfirm --clean --windowed --onedir --log-level WARN --add-data "App:." --icon App/imports/easyDiffraction/Resources/Icons/App.icns
pyinstaller App/easyDiffraction.py --noconfirm --clean --windowed --onedir --log-level WARN --add-data "App:." --icon App/imports/easyDiffraction/Resources/Icons/App.icns

read -p "Press any key to exit..."
exit 0
