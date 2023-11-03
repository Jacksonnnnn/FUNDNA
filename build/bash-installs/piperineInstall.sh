workingDir=${pwd}
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
export NUPACKHOME=~/nupack3.0.6/
cd ${NUPACKHOME} || (echo "Nupack 3.0.6 is not downloaded correctly, unable to install..." && exit)
make
python3 -m pip install .
python3 -m pip show nupack
python3 -m pytest -v --pyargs nupack
