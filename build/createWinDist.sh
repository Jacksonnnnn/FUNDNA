#!/bin/bash

# REMOVE OLD FILES
rm -r build
rm -r dist
rm -r nuskell-master
rm "nuskell-jphuse.zip"
rm "FUNDNA.spec"
rm "FUNDNA --debug.spec"

# DOWNLOAD REQUIRED FILES
mkdir dist
cd dist
mkdir assets
mkdir tests
cd ../
curl -o "dist/assets/result.png" https://gyazo.com/ae77ab94a7eccb8f8c6603be45aa1020.png
curl -o "dist/assets/taylor.png" https://gyazo.com/a0c666e23c31024e4b5097f626d550e0.png
curl -o "dist/assets/rearranged.png" https://gyazo.com/f5846f1ed0e124ad66cb5690437a8cd8.png

# INSTALL REQUIRED DEPENDENCIES
python3 -m pip install --upgrade scipy
python3 -m pip install --upgrade networkx
python3 -m pip install --upgrade matplotlib
python3 -m pip install --upgrade tk
python3 -m pip install --upgrade pathlib
python3 -m pip install --upgrade sympy
python3 -m pip install --upgrade Pillow
python3 -m pip install --upgrade mpmath
python3 -m pip install --upgrade schemdraw
python3 -m pip install --upgrade pyinstaller

# INSTALL NUSKELL
curl -o "nuskell-jphuse.zip" https://github.com/jphuse/nuskell/archive/refs/heads/master.zip
unzip nuskell-jphuse.zip
cd nuskell-master
python3 -m pip install --upgrade dsdobjects
python3 -m pip install --upgrade pytest
python3 -m pip install .[dev]
python3 -m pytest

# PYINSTALL GUI EXECUTABLES
pyinstaller gui.py Function.py FuncTypes.py GateTypes.py NotGateTypes.py RearrangeType.py Util.py --name "FUNDNA --debug" --clean --onefile --icon "assets/UK logo-white.png" --add-data "assets/*.png;assets" --hidden-import=scipy --hidden-import=networkx --hidden-import=matplotlib --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=pathlib --hidden-import=sympy --hidden-import=mpmath --hidden-import=tk --hidden-import=Schemdraw --debug=imports
pyinstaller gui.py Function.py FuncTypes.py GateTypes.py NotGateTypes.py RearrangeType.py Util.py --name "FUNDNA" --clean -w --onefile --icon "assets/UK logo-web.png" --splash "assets/FUNDNA Splash Page.png" --add-data "assets/*.png;assets" --hidden-import=scipy --hidden-import=networkx --hidden-import=matplotlib --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=pathlib --hidden-import=sympy --hidden-import=mpmath --hidden-import=tk --hidden-import=Schemdraw --debug=imports
read