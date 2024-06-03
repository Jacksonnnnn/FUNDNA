#!/bin/bash
echo "***** Installing required dependencies..."
echo ""

cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"
echo "Script directory: $SCRIPT_DIR"

# Uninstall all dependencies to ensure version correctness,
# then install required Python packages
python3 -m ensurepip --upgrade
# python3.12 get-pip.py
python3 -m pip install --upgrade pip
python3 -m pip uninstall -y -r requirements.txt
python3 -m pip uninstall -y peppercompiler
python3 -m pip uninstall -y piperine
python3 -m pip uninstall -y stickydesign
python3 -m pip install --upgrade -r requirements.txt

echo ""
echo ""
echo "***** Installing Nuskell..."
echo ""

# Uninstall previous:
cd ../
rm -r nuskell-cutlabs
echo ""
echo ""

# Install Nuskell
mkdir nuskell-cutlabs
echo ""
echo "    *** Directory made"
cd nuskell-cutlabs
git clone https://github.com/CUT-Labs/nuskell.git
echo ""
echo "    *** Repository Cloned"
cd nuskell
echo ""
echo "    *** Installing nuskell DEV..."
python3 -m pip install -U --no-deps .[dev]
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

# Install additional dependencies manually

# Install NumPy
python3 -m pip uninstall -y numpy
pip uninstall -y numpy

# Install SciPy
python3 -m pip uninstall -y scipy
pip uninstall -y scipy

# Install NUPACK
echo "    *** Installing NUPACK"
echo ""
echo "Please download NUPACK 3.0.6 from https://nupack.org/downloads to your home directory ($HOME). Once downloaded, extract into /nupack3.0.6/ and then press ENTER:"
read
tar -xvf "$HOME/nupack3.0.6.tar"
cd "$NUPACKHOME" || (echo "NUPACK 3.0.6 is not downloaded correctly, unable to install... Please make sure NUPACK is unzipped correctly and is located at $NUPACKHOME" && read)
export NUPACKHOME="$HOME/nupack3.0.6/"
make

# Install Piperine
# shellcheck disable=SC2164
cd "$SCRIPT_DIR"
echo ""
echo "    *** Installing Piperine"
python3 -m pip uninstall -y -r piperine_requirements.txt
python3 -m pip uninstall -y peppercompiler
python3 -m pip uninstall -y piperine
python3 -m pip uninstall -y stickydesign
python3 -m pip install --no-cache-dir -r piperine_requirements.txt

piperine-design --help

echo ""
echo ""
echo "***** Installation Complete!"

read
