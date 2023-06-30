cd ../
echo "***** Removing old files..."
echo ""
# REMOVE OLD FILES
rm -r build
rm -r dist
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
echo "***** Generating FUNDNA GUI Executables..."
echo ""
# PYINSTALL GUI EXECUTABLES
echo ""
echo "    *** FUNDNA --debug.exe..."
pyinstaller gui.py Function.py FuncTypes.py GateTypes.py NotGateTypes.py RearrangeType.py Util.py --name "FUNDNA --debug" --clean --onefile --icon "assets/UK logo-white.png" --add-data "assets/*.png;assets" --hidden-import=scipy --hidden-import=networkx --hidden-import=matplotlib --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=pathlib --hidden-import=sympy --hidden-import=mpmath --hidden-import=tk --hidden-import=schemdraw --debug=imports
echo ""
echo "    *** FUNDNA.exe..."
pyinstaller gui.py Function.py FuncTypes.py GateTypes.py NotGateTypes.py RearrangeType.py Util.py --name "FUNDNA" --clean -w --onefile --icon "assets/UK logo-web.png" --splash "assets/FUNDNA Splash Page.png" --add-data "assets/*.png;assets" --hidden-import=scipy --hidden-import=networkx --hidden-import=matplotlib --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=pathlib --hidden-import=sympy --hidden-import=mpmath --hidden-import=tk --hidden-import=schemdraw --debug=imports
read