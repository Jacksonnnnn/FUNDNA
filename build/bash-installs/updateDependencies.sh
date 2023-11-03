#!/bin/bash
cd ../
rm -r nuskell-cutlabs
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
python3 -m pip install --upgrade tkdesigner

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
echo "    *** Running Nuskell Help Command..."
nuskell --help

echo ""
echo ""
echo "***** Installation Complete!"
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

read