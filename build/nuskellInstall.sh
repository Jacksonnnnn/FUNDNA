# INSTALL NUSKELL
rm -r nuskell-jphuse
mkdir nuskell-jphuse
cd nuskell-jphuse
git clone https://github.com/jphuse/nuskell.git
cd nuskell
python3 -m pip install --upgrade dsdobjects
python3 -m pip install --upgrade pytest
python3 -m pip install .[dev]
python3 -m pytest

read