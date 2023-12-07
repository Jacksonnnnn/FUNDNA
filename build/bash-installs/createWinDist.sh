#!/bin/bash
echo "-------------------"
echo "FUNDNA Installation"
echo "-------------------"

# Call updateDependencies.sh
echo "***** Updating Dependencies..."
./updateDependencies.sh

# Call generateEXEs.sh
echo "***** Generating EXE files..."
./generateEXEs.sh

echo "***** Windows Distribution Created!"
read