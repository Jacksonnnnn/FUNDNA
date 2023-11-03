#!/bin/bash
echo "-------------------"
echo "FUNDNA Installation"
echo "-------------------"
cd ../
echo "***** Removing old files..."
echo ""
# REMOVE OLD FILES
rm -r build
rm -r dist
rm -r nuskell-cutlabs
rm "nuskell-cutlabs.zip"
rm "FUNDNA.spec"
rm "FUNDNA --debug.spec"

echo ""
echo ""
echo "***** Downloading required files..."
echo ""
# DOWNLOAD REQUIRED FILES
mkdir dist
cd dist
mkdir assets
mkdir tests
cd ../
curl -o "dist/assets/result.png" https://gyazo.com/ae77ab94a7eccb8f8c6603be45aa1020.png
curl -o "dist/assets/taylor.png" https://gyazo.com/a0c666e23c31024e4b5097f626d550e0.png
curl -o "dist/assets/rearranged.png" https://gyazo.com/f5846f1ed0e124ad66cb5690437a8cd8.png

echo ""
echo ""
echo "***** Installing required dependencies..."
echo ""
# INSTALL REQUIRED DEPENDENCIES
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
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

echo ""
echo ""
echo "***** Installing Nuskell..."
echo ""
# INSTALL NUSKELL
mkdir nuskell-cutlabs
echo ""
echo "    *** Directory made"
cd nuskell-cutlabs
git clone https://github.com/CUT-Labs/nuskell.git
echo ""
echo "    *** Repository Cloned"
cd nuskell
echo ""
echo "    *** Installing dependencies..."
python3 -m pip install --upgrade dsdobjects
python3 -m pip install --upgrade pytest
echo ""
echo "    *** Installing nuskell DEV..."
python3 -m pip install .[dev]
echo ""
echo "    *** Running pytest..."
python3 -m pytest


echo ""
echo ""
echo "***** Installing Piperine..."
echo ""

echo ""
echo "    *** Installing Dependencies"
python3 -m pip install --upgrade numpy scipy
python3 -m pip install --upgrade git+https://github.com/DNA-and-Natural-Algorithms-Group/peppercompiler.git
python3 -m pip install --upgrade git+https://github.com/DNA-and-Natural-Algorithms-Group/stickydesign.git
echo ""

echo "    *** Installing NUPACK"
python3 -m pip install --upgrade matplotlib jupyterlab
echo ""
echo "Please download NUPACK 3.0.6 from https://nupack.org/downloads to your home directory (${HOME}) and then press ENTER:"
read
tar -xvf "${HOME}/nupack3.0.6.tar"
cd ${NUPACKHOME} || (echo "NUPACK 3.0.6 is not downloaded correctly, unable to install... Please make sure NUPACK is unzipped correctly and is located at ${NUPACKHOME}" && read)
export NUPACKHOME="${HOME}/nupack3.0.6/"
make

echo ""
echo "    *** Installing Piperine"
python3 -m pip install --upgrade git+https://github.com/DNA-and-Natural-Algorithms-Group/piperine.git


echo ""
echo ""
echo "***** Generating FUNDNA GUI Executables..."
echo ""
# PYINSTALL GUI EXECUTABLES
cd ../../
echo ""
echo "    *** FUNDNA --debug.exe..."
pyinstaller gui.py Function.py FuncTypes.py GateTypes.py NotGateTypes.py RearrangeType.py Util.py --name "FUNDNA --debug" --clean --onefile --icon "assets/UK logo-white.png" --splash "assets/FUNDNA Splash Page.png" --add-data "assets/*.png;assets" --hidden-import=scipy --hidden-import=networkx --hidden-import=matplotlib --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=pathlib --hidden-import=sympy --hidden-import=mpmath --hidden-import=tk --hidden-import=schemdraw --debug=imports
echo ""
echo "    *** FUNDNA.exe..."
pyinstaller gui.py Function.py FuncTypes.py GateTypes.py NotGateTypes.py RearrangeType.py Util.py --name "FUNDNA" --clean -w --onefile --icon "assets/UK logo-web.png" --splash "assets/FUNDNA Splash Page.png" --add-data "assets/*.png;assets" --hidden-import=scipy --hidden-import=networkx --hidden-import=matplotlib --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=pathlib --hidden-import=sympy --hidden-import=mpmath --hidden-import=tk --hidden-import=schemdraw --debug=imports

echo ""
echo ""
echo "***** Installation Complete!"
read