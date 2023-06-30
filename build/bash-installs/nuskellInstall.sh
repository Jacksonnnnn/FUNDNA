cd ../
echo "***** Removing old files..."
echo ""
rm -r nuskell-jphuse

echo ""
echo ""
echo "***** Installing Nuskell..."
echo ""
# INSTALL NUSKELL
mkdir nuskell-jphuse
echo ""
echo "    *** Directory made"
cd nuskell-jphuse
git clone https://github.com/jphuse/nuskell.git
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

read