#!/bin/sh
clear

CURRENT_DIR="$(dirname "$0")"
VENV_DIR=$CURRENT_DIR/.python-venv

echo "*** activate virtual environment: $VENV_DIR"
source $VENV_DIR/bin/activate

echo "*** upgrade pip"
pip install --upgrade pip

echo "*** install Qt for Python (pyside2 and shiboken2)"
pip install PySide2

echo "*** install scipy"
pip install scipy

echo "*** install numpy"
#pip install numpy
##pip uninstall numpy
pip install numpy==1.16.4 # 1.17 gives error: No module named 'numpy.random.common'

echo "*** install PyInstaller"
#pip install pyinstaller
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz

read -p "Press any key to exit..."
exit 0
