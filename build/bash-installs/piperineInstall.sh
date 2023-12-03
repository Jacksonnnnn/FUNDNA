echo ""
echo ""
echo "***** Installing Piperine..."
echo ""

echo ""
echo "    *** Installing Dependencies"

# PYTHON Must be at a maximum 2.7 - 3.7
# NUMPY Must be 1.16
# SCIPY Can be latest version
# PEPPERCOMPILER Must be 0.1.2 (Git branch: c2c5f4a672b789377d4417ec0f828c78e9c91316)
# STICKYDESIGN Must be 0.7.0
# NUPACK Must be 3.0.6
# JUPYTERLAB Can be latest version
# MATPLOTLIB Can be latest version
python3 -m pip install numpy==1.16
python3 -m pip install --upgrade scipy
python3 -m pip install --upgrade git+https://github.com/DNA-and-Natural-Algorithms-Group/peppercompiler.git@c2c5f4a672b789377d4417ec0f828c78e9c91316
python3 -m pip install stickydesign==0.7.0
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

piperine-design --help

echo ""
echo ""
echo "***** Installation Complete!"