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
tar -xvf "${HOME}/nupack3.0.6.tar"
cd ${NUPACKHOME} || (echo "NUPACK 3.0.6 is not downloaded correctly, unable to install... Please make sure NUPACK is unzipped correctly and is located at ${NUPACKHOME}" && read)
export NUPACKHOME="${HOME}/nupack3.0.6/"
make

echo ""
echo "    *** Installing Piperine"
python3 -m pip install --upgrade git+https://github.com/DNA-and-Natural-Algorithms-Group/piperine.git